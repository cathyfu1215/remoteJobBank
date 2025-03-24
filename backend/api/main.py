from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.params import Path as FastAPIPath
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
import os
import sys
from pathlib import Path
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from urllib.parse import unquote

# Add parent directory to path to import scraper modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add project root directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from scraper.schema import ALLOWED_CATEGORIES, validate_job_data

"""Remote Job Bank API Module.

This module provides a FastAPI application that serves as an API for retrieving
and managing remote job listings. It connects to a Firestore database to store
and retrieve job data.

Typical usage:
    uvicorn backend.api.main:app --reload
"""

# Load environment variables
dotenv_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path)

app = FastAPI(
    title="Remote Job Bank API",
    description="API for retrieving and managing remote job listings",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import Firebase client
from backend.database.firebase_client import get_firestore_client, exists_in_collection, save_to_collection

# Get Firestore client
db = get_firestore_client()

class JobData(BaseModel):
    """Schema for job posting data.
    
    This Pydantic model defines the structure and validation rules for job data
    in the API requests and responses.
    
    Attributes:
        job_id: Unique identifier for the job posting.
        title: The job title.
        company: The name of the hiring company.
        company_about: Short description of the company.
        apply_url: URL where users can apply for the job.
        apply_before: Deadline for job applications.
        job_description: Detailed description of the job.
        category: Job category (must be one of the allowed categories).
        region: Geographic region(s) where the job is available.
        salary_range: The salary range for the position (default: "Not Specified").
        countries: List of countries where the job is available.
        skills: List of required skills for the job.
        timezones: List of accepted time zones for the job.
        url: Optional original URL where the job was found.
        source: Optional source of the job listing.
        timestamp: Optional timestamp when the job was scraped or added.
    """
    job_id: str
    title: str
    company: str
    company_about: str
    apply_url: str
    apply_before: str
    job_description: str
    category: str
    region: Union[str, List[str]]
    salary_range: str = "Not Specified"
    countries: List[str] = []
    skills: List[str] = []
    timezones: List[str] = []
    url: Optional[str] = None
    source: Optional[str] = None
    timestamp: Optional[datetime] = None


class PaginatedResponse(BaseModel):
    """Schema for paginated response data.
    
    This model defines the structure for paginated API responses.
    
    Attributes:
        items: List of items (jobs) for the current page.
        total: Total number of items across all pages.
        page: Current page number.
        size: Number of items per page.
        pages: Total number of pages.
    """
    items: List[JobData]
    total: int
    page: int
    size: int
    pages: int


async def admin_required(api_key: str = Query(..., alias="api_key")):
    """Dependency for admin authentication.
    
    Verifies that the request includes a valid admin API key.
    
    Args:
        api_key: The API key provided in the request query parameter.
        
    Returns:
        bool: True if authentication is successful.
        
    Raises:
        HTTPException: If the API key is invalid, with a 403 status code.
    """
    admin_key = os.getenv("ADMIN_API_KEY", "default_admin_key")
    if api_key != admin_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized"
        )
    return True


def paginate_results(items: List[Dict], page: int = 1, size: int = 10) -> Dict[str, Any]:
    """Paginates a list of items.
    
    Takes a list of items and returns a paginated subset based on the
    requested page and page size.
    
    Args:
        items: The full list of items to paginate.
        page: The requested page number (starting from 1).
        size: The number of items per page.
        
    Returns:
        Dict containing the paginated items, total count, current page,
        page size, and total number of pages.
    """
    total = len(items)
    pages = (total + size - 1) // size  # Ceiling division
    
    start = (page - 1) * size
    end = start + size
    
    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }


@app.get("/data", response_model=PaginatedResponse)
async def get_all_jobs(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page")
):
    """Retrieve all scraped job data with pagination.
    
    Args:
        page: The page number to retrieve (starting from 1).
        size: The number of items per page (between 1 and 100).
        
    Returns:
        A PaginatedResponse object containing the requested jobs and pagination metadata.
        
    Raises:
        HTTPException: If there's an error retrieving data from Firestore.
    """
    try:
        # Get all documents from the 'jobs' collection
        jobs_ref = db.collection('jobs')
        docs = jobs_ref.stream()
        
        # Convert to list of dictionaries
        jobs = [doc.to_dict() for doc in docs]
        
        # Apply pagination
        paginated = paginate_results(jobs, page, size)
        
        return paginated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving data: {str(e)}"
        )


@app.get("/data/{param}", response_model=PaginatedResponse)
async def get_filtered_data(
    param: str = FastAPIPath(..., description="Category or company name"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page")
):
    """Retrieve job data filtered by category or company name.
    
    This endpoint handles two types of filtering:
    1. If param matches a valid category, it returns all jobs in that category
    2. If param doesn't match a category, it's treated as a company name search
    
    Args:
        param: The category or company name to filter by.
        page: The page number to retrieve (starting from 1).
        size: The number of items per page (between 1 and 100).
        
    Returns:
        A PaginatedResponse object containing the filtered jobs and pagination metadata.
        
    Raises:
        HTTPException: If there's an error retrieving or filtering data.
    """
    try:
        # Decode URL parameter and normalize it
        decoded_param = unquote(param)
        
        # Check if param is a valid category
        if decoded_param in ALLOWED_CATEGORIES or decoded_param == "All Other Remote Jobs":
            # This is a category request
            jobs_ref = db.collection('jobs').where('category', '==', decoded_param)
            docs = jobs_ref.stream()
            jobs = [doc.to_dict() for doc in docs]
            
            # For debugging
            print(f"Category search for '{decoded_param}' found {len(jobs)} jobs")
            
            return paginate_results(jobs, page, size)
        else:
            # This is a company request - Firestore doesn't support case-insensitive search
            # so we'll fetch all documents and filter in memory
            jobs_ref = db.collection('jobs')
            docs = jobs_ref.stream()
            
            # Convert to list and filter for case-insensitive company match
            all_jobs = [doc.to_dict() for doc in docs]
            jobs = [
                job for job in all_jobs 
                if decoded_param.lower() in job.get('company', '').lower()
            ]
            
            # For debugging
            print(f"Company search for '{decoded_param}' found {len(jobs)} jobs")
            
            return paginate_results(jobs, page, size)
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving data: {str(e)}"
        )


@app.delete("/data/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: str = FastAPIPath(..., description="Job ID to delete"),
    _: bool = Depends(admin_required)
):
    """Delete a specific job entry (admin functionality).
    
    This endpoint requires admin authentication via API key.
    
    Args:
        job_id: The unique identifier of the job to delete.
        _: Result of admin_required dependency (not used directly).
        
    Returns:
        None on successful deletion.
        
    Raises:
        HTTPException: If the job doesn't exist (404) or there's an error during deletion (500).
    """
    try:
        # Get the job document reference
        job_ref = db.collection('jobs').document(job_id)
        
        # Check if the job exists
        job = job_ref.get()
        if not job.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job with ID {job_id} not found"
            )
        
        # Delete the job
        job_ref.delete()
        
        return None
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting job: {str(e)}"
        )


@app.get("/data/search", response_model=PaginatedResponse)
async def search_jobs(
    title: Optional[str] = Query(None, description="Search in job title"),
    description: Optional[str] = Query(None, description="Search in job description"),
    skills: Optional[str] = Query(None, description="Search for specific skills"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page")
):
    """Search for jobs based on various criteria.
    
    This endpoint allows searching job listings by title, description, or skills.
    Multiple filters can be applied simultaneously (logical AND).
    
    Args:
        title: Text to search for in job titles.
        description: Text to search for in job descriptions.
        skills: Text to search for in job required skills.
        page: The page number to retrieve (starting from 1).
        size: The number of items per page (between 1 and 100).
        
    Returns:
        A PaginatedResponse object containing the matching jobs and pagination metadata.
        
    Raises:
        HTTPException: If there's an error during the search process.
        
    Note:
        This implementation fetches all data and filters in memory. For production,
        consider using a proper search engine for better performance.
    """
    try:
        # Start with the base collection
        jobs_ref = db.collection('jobs')
        
        # Apply filters if provided
        # Note: Firestore doesn't support complex queries like CONTAINS
        # This is a workaround that fetches all data and filters in memory
        docs = jobs_ref.stream()
        jobs = [doc.to_dict() for doc in docs]
        
        # Apply filters in memory
        filtered_jobs = jobs
        
        if title:
            filtered_jobs = [
                job for job in filtered_jobs 
                if title.lower() in job.get('title', '').lower()
            ]
            
        if description:
            filtered_jobs = [
                job for job in filtered_jobs 
                if description.lower() in job.get('job_description', '').lower()
            ]
            
        if skills:
            filtered_jobs = [
                job for job in filtered_jobs 
                if any(skills.lower() in skill.lower() for skill in job.get('skills', []))
            ]
            
        # Apply pagination
        paginated = paginate_results(filtered_jobs, page, size)
        
        return paginated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching jobs: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint to verify API is running.
    
    Returns:
        Dict containing status ("healthy") and current timestamp.
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 