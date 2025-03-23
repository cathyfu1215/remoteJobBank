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
remoteJobBank/
├── README.md                # Main project documentation and setup instructions
├── design-choices.md        # Document explaining design choices and time spent
├── ai-prompts.md            # Documentation of AI tools used
├── docker-compose.yml       # For easy setup and demonstration
│
├── backend/                 # FastAPI backend and scraper
│   ├── README.md            # Backend-specific instructions
│   ├── requirements.txt     # Python dependencies
│   ├── main.py              # FastAPI application entry point
│   ├── scraper/             # Selenium scraping code
│   │   └── scraper.py       # Main scraper implementation
│   │
│   ├── database/            # Database models and connections
│   │   └── firebase.py      # Firebase connection and operations
│   │
│   └── api/                 # FastAPI routes
│       └── routes.py        # API endpoints
│
└── frontend/                # React frontend
    ├── README.md            # Frontend-specific instructions
    ├── package.json         # JavaScript dependencies
    ├── public/              # Static assets
    │   └── index.html       # HTML entry point
    │
    └── src/                 # React source code
        ├── index.js         # JavaScript entry point
        ├── App.js           # Main application component
        ├── components/      # Reusable UI components
        │   ├── JobCard.jsx  # Job listing component
        │   └── JobFilter.jsx# Filtering component
        │
        └── services/        # API client
            └── api.js       # Backend API integration
```


## Installation


## Usage


## Disclaimer  
This project is created for educational purposes only. While scraping data from [We Work Remotely](https://weworkremotely.com), I have strictly followed the guidelines outlined in their `robots.txt` file.  

I do not intend to misuse or distribute the scraped data commercially. If there are any concerns regarding data usage, please contact me, and I will take appropriate action.
