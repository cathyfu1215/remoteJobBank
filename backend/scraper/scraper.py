import os
import time
import requests
from datetime import datetime
from urllib.parse import urlparse
from xml.etree import ElementTree
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
from .schema import validate_job_data



# Load environment variables from .env file
dotenv_path = Path(__file__).resolve().parent.parent.parent / ".env"
# Load environment variables
load_dotenv()

# Firebase initialization
firebase_cred = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
}

cred = credentials.Certificate(firebase_cred)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Configure Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def get_driver():
    return webdriver.Chrome(options=chrome_options)

def parse_sitemap(url):
    job_urls = []
    try:
        response = requests.get(url, timeout=10)
        root = ElementTree.fromstring(response.content)
        
        for child in root:
            if 'sitemap' in child.tag:
                loc = child[0].text
                if 'job-sitemap' in loc:
                    job_urls.extend(parse_sitemap(loc))
            elif 'loc' in child.tag:
                job_urls.append(child.text)
        
        return job_urls
    except Exception as e:
        print(f"Error parsing sitemap: {e}")
        return []

def extract_job_data(url, driver):
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'listing-header-container'))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        parsed_url = urlparse(url)
        
        # Extract category from URL (example: /categories/2-programming)
        category = "Other"
        url_parts = parsed_url.path.split('/')
        if len(url_parts) > 2 and url_parts[1] == 'categories':
            category = url_parts[2].split('-')[1].title()
        
        job_data = {
            'job_id': parsed_url.path.split('/')[-1],
            'title': soup.find('h1', class_='listing-header-container').get_text(strip=True),
            'company': soup.find('h2', class_='company').get_text(strip=True) if soup.find('h2', class_='company') else '',
            'location': soup.find('h3', class_='location').get_text(strip=True) if soup.find('h3', class_='location') else 'Remote',
            'description': soup.find('div', id='job-description').get_text(strip=True) if soup.find('div', id='job-description') else '',
            'url': url,
            'posted_at': firestore.SERVER_TIMESTAMP,
            'source': 'WeWorkRemotely',
            'category': category,
            'active': True,
            # Optional fields
            'salary_range': soup.find('span', class_='salary').get_text(strip=True) if soup.find('span', class_='salary') else 'Not Specified',
            'tags': [tag.get_text(strip=True) for tag in soup.find_all('li', class_='tag')],
            'application_email': soup.find('a', class_='apply')['href'].split('mailto:')[-1] if soup.find('a', class_='apply') else ''
        }
        
        return job_data
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        print(f"Error scraping {url}: {e}")
        return None

def save_to_firestore(job_data):
    try:
        # Create unique ID from URL
        parsed_url = urlparse(job_data['url'])
        doc_id = parsed_url.path.split('/')[-1]
        
        doc_ref = db.collection('jobs').document(doc_id)
        if not doc_ref.get().exists:
            doc_ref.set(job_data)
            print(f"Saved new job: {doc_id}")
        else:
            print(f"Job already exists: {doc_id}")
    except Exception as e:
        print(f"Firestore error: {e}")

def main():
    driver = get_driver()
    
    try:
        sitemap_url = "https://weworkremotely.com/sitemap.xml"
        job_urls = parse_sitemap(sitemap_url)
        print(f"Found {len(job_urls)} job URLs")
        
        for url in job_urls:
            raw_data = extract_job_data(url, driver)
            if raw_data:
                try:
                    validated_data = validate_job_data(raw_data)
                    save_to_firestore(validated_data)
                except ValueError as e:
                    print(f"Skipping invalid job data: {e}")
                except Exception as e:
                    print(f"Unexpected error validating data: {e}")
            time.sleep(3)
            
    finally:
        driver.quit()
        print("Scraping completed")

