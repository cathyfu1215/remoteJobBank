# RemoteJobBank
This is Cathy's full stack project that contains:
- Job information scraped from [We Work Remotely](https://weworkremotely.com), stored in database with
  - well-structured schema
  - handles duplicates
  - ensures data integrity
- a RESTful API that supports filtering, pagination
- a simple, user-friendly user interface.


## Documents
- [design choices and time logs](https://github.com/cathyfu1215/remoteJobBank/blob/main/design-choices.md)
- [AI prompts](https://github.com/cathyfu1215/remoteJobBank/blob/main/ai-prompts.md)



## Tech Stack
- Frontend: React 
- Backend: FastAPI
- Database: Google Firebase
- Scraper: Selenium


## Features
- Scrapes job data from We Work Remotely using Selenium
- Stores the data to firebase
- RESTful API that has routes:
  - GET /data → Retrieve all scraped data
  - GET /data/{category} → Retrieve data filtered by category
  - GET /data/{company} → Retrieve data by company name (if applicable)
  - (due to time comstraints, I did not implement the delete function because it needs authentication)
- Frontend that
  - fetches and displays data from the API
  - provide filtering options



## Installation

### Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop/) installed on your machine
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/remoteJobBank.git
   cd remoteJobBank
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up
   ```
   The first run will take a few minutes as it builds the Docker images.

3. **Access the application**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

### Stopping the Application

To stop the application, press `Ctrl+C` in the terminal where it's running, or run:
```bash
docker-compose down
```

### Rebuilding After Changes

If you make changes to the code and want to rebuild:
```bash
docker-compose up --build
```

### Troubleshooting

- **Port conflicts**: If ports 3000 or 8000 are already in use on your machine, modify the `ports` section in docker-compose.yml
- **Container crashes**: Check the logs with `docker logs remoteJobBank-app-1`
- **Slow performance**: First run may be slower while Docker builds the image and the React app



## Disclaimer  
This project is created for educational purposes only. While scraping data from [We Work Remotely](https://weworkremotely.com), I have strictly followed the guidelines outlined in their `robots.txt` file.  

I do not intend to misuse or distribute the scraped data commercially. If there are any concerns regarding data usage, please contact me, and I will take appropriate action.
