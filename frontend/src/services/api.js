const API_BASE_URL = 'http://localhost:8000';

// Fetch jobs with pagination and optional filtering
export async function fetchJobs(page = 1, size = 10, filterType = null, filterValue = null) {
  try {
    let url = '';
    
    if (filterType && filterValue) {
      // For category or company filtering
      url = `${API_BASE_URL}/data/${encodeURIComponent(filterValue)}?page=${page}&size=${size}`;
    } else {
      // For all jobs
      url = `${API_BASE_URL}/data?page=${page}&size=${size}`;
    }
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching jobs:', error);
    throw error;
  }
}

// Fetch job categories from schema
export async function fetchCategories() {
  try {
    // This is normally an API call, but since we already know the categories
    // from the schema.py file, we can hardcode them
    return [
      "Programming",
      "Full-Stack Programming",
      "Front-End Programming",
      "Back-End Programming", 
      "DevOps and Sysadmin",
      "Management and Finance",
      "Product",
      "Customer Support",
      "Sales and Marketing",
      "All Other Remote Jobs"
    ];
  } catch (error) {
    console.error('Error fetching categories:', error);
    throw error;
  }
}

// Fetch a single job by ID
export async function fetchJobById(jobId) {
  try {
    const response = await fetch(`${API_BASE_URL}/data/${jobId}`);
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`Error fetching job ${jobId}:`, error);
    throw error;
  }
}
