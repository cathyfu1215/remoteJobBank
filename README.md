# remoteJobBank
This is a full stack project that contains:
- Job information scraped from [We Work Remotely](https://weworkremotely.com), stored in database with
  - well-structured schema
  - andles duplicates
  - ensures data integrity
- a RESTful API that supports filtering, pagination
- a simple, user-friendly user interface.

## Tech Stack
- Frontend: Next.js
- Backend: FastAPI
- Database: Google Firebase
- Scraper: Selenium

## Repo Structure 
```
project-root/
├── README.md            # Main project documentation and setup instructions
├── design-choices.md    # Document explaining design choices and time spent
├── ai-prompts.md        # Documentation of AI tools used (as required)
├── backend/             # FastAPI backend and scraper
│   ├── scraper/         # Selenium scraping code
│   ├── database/        # Database models and connections
│   ├── api/             # FastAPI routes
│   ├── requirements.txt # Python dependencies
│   └── README.md        # Backend-specific instructions
├── frontend/            # React frontend
│   ├── src/             # React components
│   ├── package.json     # JavaScript dependencies
│   └── README.md        # Frontend-specific instructions
└── docker-compose.yml   # (Optional) For easy setup and demonstration
```


## Installation


## Usage


## Disclaimer  
This project is created for educational purposes only. While scraping data from [We Work Remotely](https://weworkremotely.com), I have strictly followed the guidelines outlined in their `robots.txt` file.  

I do not intend to misuse or distribute the scraped data commercially. If there are any concerns regarding data usage, please contact me, and I will take appropriate action.
