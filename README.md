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

## Screenshots
![Screenshot 2025-03-23 at 10 39 34 PM](https://github.com/user-attachments/assets/1348e52c-17c6-4090-8fbf-c78a4b65c49a)

![Screenshot 2025-03-23 at 10 40 54 PM](https://github.com/user-attachments/assets/339133ac-1321-4381-96f0-33437445d768)

![Screenshot 2025-03-23 at 10 41 07 PM](https://github.com/user-attachments/assets/ab3d432d-ba35-4817-b157-105596526b91)

## Installation

### Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop/) installed on your machine
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/cathyfu1215/remoteJobBank.git
   cd remoteJobBank
   ```
2. **Create ```.env``` file**
   ```
   # Create new .env file in the ROOT folder
    touch .env  # Linux/macOS
   # Windows users: Right-click → New → Text Document → Rename to ".env"
   
   ```
3. **Add your firebase credentials to the ```.env``` file**
   The .env file should look like: 
   ```
   # .env.example

    FIREBASE_TYPE=service_account
    FIREBASE_PROJECT_ID=your_project_id
    FIREBASE_PRIVATE_KEY_ID=your_private_key_id
    FIREBASE_PRIVATE_KEY=your_private_key
    FIREBASE_CLIENT_EMAIL=your_client_email
    FIREBASE_CLIENT_ID=your_client_id
    FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
    FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
    FIREBASE_CLIENT_X509_CERT_URL=your_client_x509_cert_url

 
   ```
    and save the .env

   
5. **Run with Docker Compose**
   ```bash
   docker-compose up --build
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
- **Slow performance**: First run may be slower while Docker builds the image and the React app



## Disclaimer  
This project is created for educational purposes only. While scraping data from [We Work Remotely](https://weworkremotely.com), I have strictly followed the guidelines outlined in their `robots.txt` file.  

I do not intend to misuse or distribute the scraped data commercially. If there are any concerns regarding data usage, please contact me, and I will take appropriate action.
