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
3. **Add firebase credentials to the ```.env``` file**
   ```
   
   # .env
   FIREBASE_TYPE=service_account
    FIREBASE_PROJECT_ID=remotejobbank
    FIREBASE_PRIVATE_KEY_ID=05dbca93ee50635533d1c5196bbc42b726738447
    FIREBASE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCR7MZ/A1/6cQGT\n9WwNyrwGP82DQYkP/AHCpncSgtpzJYNpLfMJcIDvk3sKHWOdnXNrTD44ZFUeQGM1\n6guwriNyLThuwbvu0FMDR7DiQHXHsXuD38u1H8Sbc7LQdjluvHfsHIocctGUNzo0\nBxLATVvUtD3L5L72xZWoRxMAGGT9awpj5nbmxl/TH/Xt9ZSowZf7G1XthQkGGHsj\nx6jpRLkmIa8MbEXosb1eTECHXcgb6hjeIvTkJ+cMWgGxsjJLCXI/lpjWRCNJyVpe\nHyMjZsTPEQRi86i7CxQtxXyMoZxx8s6qEU2ELKfBOJttMf3IWbh6V3Dn8Is6AUfD\nJZ12GwopAgMBAAECggEACJasPyUCdOHKUzxGYhBs3RxLuv40NDfjnaKBDxqbA1xx\nndLpw0Q3HoKqYvfEWW4/MRFBdz22gcuN20o9amZxaSKut9wYtM9Xl3GUgFiFZh20\n1JfrLCukvXaDj3/p1PHsR/4NBewfGC9g8ld5O87BySTbn0DFGY6bBpa6UE7fQMgB\nhedj4qdwdu6YRq50+5LPIg+2441CRKMxAaD2I7EnXv+Gm0HZnTg4VRl2O2GI9eeR\nKybdZLLU+iYWbxUlV8AyTAsuZY1wVzIVVrPMnRpb5BHfJkwmsLOtk3mjE5vaKhTL\nfqW4IIGO6aDsBo3NLoRGYgpBY0i3D2q312ym/susoQKBgQDIjdDlVDtAnjbF2JS9\n/3MbIGtQ0vb2s21Ms0H/9RrvcrCVWItJqGQrnQoBpjAKGYq+rD7S9H8tHPeDvnKV\nKpZBDEwSqiUqBtm6qCV8PPPHEU8JHJyDNKoVgJcgJhetKcYJM7jGEv9Z6L8DxHup\npxKYOZ9saJ3FkpTE15mYxkvRcQKBgQC6RJf2rpRF27lnv5TcTPf2bvLKO9h3Tzye\nVQw0UUaBMyiE/DTzOG7IiZsXUVthj9oL2VHz8EZOhNekv3WLDFZzkc0kLif5ROYh\ngjtV+GMYqI1ac92o6UKYn+0qwdVcaa1WtrFHXWuHrGJR7ITm0QZKZHt2COHBvv/Z\nVsyEapvoOQKBgQC3YJSlXENhbkj+1m4K3ExPfXEi0gNmx+EkxLOQanlagC/eHrwd\neY8+IbVIlMBQO9KVTcGT+mNeyKG5IKZ8phgFGk1ks5aPuvvSpHTCCKmOV9FAr5yc\ni8cJKi8FAk+b0hp1x4kn867wctRViY7ZLR7febC/21iHkuPcqJaVDpu8wQKBgAIE\nmDjd71FKbhnHo483bkBHN24lc9TnENsORNGUR9VCfp/iM5im9dxKUVnRUdIewtf6\nBL9FzR0wpz1rrZRSD+W0oKpRrbEvo+adCJOH21r7CH0AYFhiHoyUvvcFnpAfvPcB\nh64kPvP7VB1bGJ1/ijfoGsZOllOJBDCQliqhFQtRAoGBAMF1fKNwyl/a6rUjbosI\n51qWSW6jNI3vBIrQ3IEhPyNZZ6mhh60bN2ygoUKeUKOfvL9Z9MZiY2pwIoqzreSy\nhrI3GZf6x7RZIbBJDUC4wn2egka/6gjRA+LVGTt++k5kfgnEBX8CQSroGy7RP4I2\nOjSFxKxJpaQh4iXokrozUF8e\n-----END PRIVATE KEY-----\n
    FIREBASE_CLIENT_EMAIL=firebase-adminsdk-fbsvc@remotejobbank.iam.gserviceaccount.com
    FIREBASE_CLIENT_ID=108196420774828988584
    FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
    FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
    FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40remotejobbank.iam.gserviceaccount.com
 
   ```
    and save the .env

   Note: I admit this is terrible design choices to put my keys here. I will rotate my credentials in one week. Please only use it when you are my potential employer :)
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
