# Description: This file contains the schema for the job data that is scraped from the job boards.
# Also it contains a function to validate the job data.


ALLOWED_CATEGORIES = {
    "Programming",
    "Design",
    "DevOps and Sysadmin",
    "Management and Finance",
    "Product",
    "Customer Support",
    "Sales and Marketing",
    "All Other Remote Jobs"
}

REQUIRED_FIELDS = ['job_id', 'title', 'company', 'company_about', 'apply_url', 'apply_before', 'job_description', 'category', 'region']

def validate_job_data(job_data):
    # Check required fields
    missing_fields = [field for field in REQUIRED_FIELDS if field not in job_data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    # Clean and validate category
    category = job_data.get('category', '').strip()
    job_data['category'] = category if category in ALLOWED_CATEGORIES else 'All Other Remote Jobs'
    
    
    # Set defaults for optional fields
    job_data.setdefault('salary_range', 'Not Specified')
    job_data.setdefault('countries', [])
    job_data.setdefault('skills', [])
    job_data.setdefault('timezones', [])
    
    return job_data