# remoteJobBank
This is a full stack project that contains:
- Job information scraped from [We Work Remotely](https://weworkremotely.com), stored in database with
  - well-structured schema
  - handles duplicates
  - ensures data integrity
- a RESTful API that supports filtering, pagination
- a simple, user-friendly user interface.

## Tech Stack
- Frontend: React 
- Backend: FastAPI
- Database: Google Firebase
- Scraper: Selenium

## Repo Structure 
```
remoteJobBank/                            # Root project directory
├── backend/                              # FastAPI backend application
│   ├── __pycache__/                      
│   ├── api/                              # API endpoints and routing
│   │   ├── __pycache__/                  
│   │   └── main.py                       # FastAPI application endpoints
│   ├── database/                         # Database connection and operations
│   │   ├── __pycache__/                  
│   │   ├── __init__.py                   
│   │   ├── firebase_client.py            # Firebase connection and operations
│   │   └── test_firebase.py              # Tests for Firebase operations
│   ├── models/                           # Data models/schemas
│   │   └── __pycache__/                  
│   ├── scraper/                          # Web scraping module
│   │   ├── __pycache__/                  
│   │   ├── schema.py                     # Database schema definitions
│   │   └── scraper.py                    # Main scraper implementation
│   └── utils/                            
├── frontend/                             # React frontend application
│   ├── public/                           # Static assets
│   │   └── index.html                    # HTML entry point
│   ├── src/                              # React source code
│   │   ├── components/                   # Reusable UI components
│   │   ├── context/                      # React context providers
│   │   ├── services/                     # API client and services
│   │   ├── App.css                       # Main component styles
│   │   ├── App.js                        # Main application component
│   │   ├── index.css                     # Global styles
│   │   └── index.js                      # JavaScript entry point
│   ├── package-lock.json                 # NPM dependency lock file
│   └── package.json                      # JavaScript dependencies
```


## Installation


## Usage


## Disclaimer  
This project is created for educational purposes only. While scraping data from [We Work Remotely](https://weworkremotely.com), I have strictly followed the guidelines outlined in their `robots.txt` file.  

I do not intend to misuse or distribute the scraped data commercially. If there are any concerns regarding data usage, please contact me, and I will take appropriate action.
