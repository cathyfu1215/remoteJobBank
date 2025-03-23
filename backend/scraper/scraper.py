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
from schema import validate_job_data  
import pprint


# Load environment variables from .env file
dotenv_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path)

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
            EC.presence_of_element_located((By.CLASS_NAME, 'listing-header-container')))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        parsed_url = urlparse(url)
        
        # Extract category from URL
        category = "All Other Remote Jobs"
        url_parts = parsed_url.path.split('/')
        if len(url_parts) > 2 and url_parts[1] == 'categories':
            raw_category = '-'.join(url_parts[2].split('-')[1:])  # Handle multi-word categories
            category = raw_category.title().replace('And', 'and')  # Maintain 'and' lowercase
            
        # Extract company info
        company_section = soup.find('div', class_='company-card')
        
        # Extract main job details
        job_data = {
            'job_id': parsed_url.path.split('/')[-1],
            'title': soup.find('h1', class_='listing-header-container').get_text(strip=True),
            'company': soup.find('h2', class_='company').get_text(strip=True),
            'company_about': company_section.get_text(strip=True) if company_section else '',
            'apply_url': soup.find('a', class_='apply')['href'] if soup.find('a', class_='apply') else '',
            'posted_on': soup.find('time').get('datetime') if soup.find('time') else '',
            'apply_before': soup.find('span', class_='deadline').get_text(strip=True) if soup.find('span', class_='deadline') else '',
            'job_description': soup.find('div', id='job-description').get_text(strip=True),
            'category': category,
            'region': soup.find('h3', class_='location').get_text(strip=True) if soup.find('h3', class_='location') else 'Remote',
            
            # Optional fields with defaults
            'salary_range': soup.find('li', class_='salary').get_text(strip=True) if soup.find('li', class_='salary') else 'Not Specified',
            'countries': [c.get_text(strip=True) for c in soup.select('.country-list li')],
            'skills': [s.get_text(strip=True) for s in soup.select('.skills-list li')],
            'timezones': [t.get_text(strip=True) for t in soup.select('.timezone-list li')],
            
            # Metadata
            'url': url,
            'source': 'WeWorkRemotely',
            'timestamp': firestore.SERVER_TIMESTAMP
        }
        
        return job_data
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        print(f"Error scraping {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error processing {url}: {e}")
        return None

def save_to_firestore(job_data, dry_run=False):
    try:
        parsed_url = urlparse(job_data['url'])
        doc_id = parsed_url.path.split('/')[-1]
        
        if dry_run:
            print("🚨 Dry Run: Would NOT save to Firestore:")
            pprint.pprint(job_data, indent=2)
            return True
        
        doc_ref = db.collection('jobs').document(doc_id)
        if not doc_ref.get().exists:
            doc_ref.set(job_data)
            print(f"Saved new job: {doc_id}")
        else:
            print(f"Job already exists: {doc_id}")
        return True
    except Exception as e:
        print(f"Firestore error: {e}")
        return False


def test_scrape(test_urls=None, dry_run=False):
    """
    Test the scraping process with specific URLs
    Usage: test_scrape(["https://example.com/job"], dry_run=True)
    """
    driver = get_driver()
    pp = pprint.PrettyPrinter(indent=2)
    
    if not test_urls:
        test_urls = [
            "https://weworkremotely.com/remote-jobs/clipboard-health-collections-account-manager-2",
            "https://weworkremotely.com/remote-jobs/laudio-staff-software-engineer",
            "https://weworkremotely.com/remote-jobs/soflyy-wordpress-developer-technical-writer",
            "https://weworkremotely.com/remote-jobs/maverick-trading-equity-option-trader-at-maverick-trading"
        ]
    
    try:
        print(f"\n{' DRY RUN ' if dry_run else ''} Starting test with {len(test_urls)} URLs")
        
        for i, url in enumerate(test_urls, 1):
            print(f"\n--- Processing URL {i}/{len(test_urls)} ---")
            print(f"URL: {url}")
            
            try:
                # Extraction
                start_time = time.time()
                raw_data = extract_job_data(url, driver)
                
                if not raw_data:
                    print("❌ No data extracted")
                    continue
                
                # Print raw data
                print("\nRaw extracted data:")
                pp.pprint(raw_data)
                
                # Validation
                try:
                    validated_data = validate_job_data(raw_data)
                    validation_time = time.time() - start_time
                    print(f"\n✅ Validated in {validation_time:.2f}s")
                    print("Validated data:")
                    pp.pprint(validated_data)
                except ValueError as e:
                    print(f"\n❌ Validation failed: {e}")
                    continue
                
                # Saving
                if not dry_run:
                    save_success = save_to_firestore(validated_data)
                    print(f"💾 Save {'succeeded' if save_success else 'failed'}")
                else:
                    save_to_firestore(validated_data, dry_run=True)
                
            except Exception as e:
                print(f"\n⚠️ Unexpected error: {str(e)}")
                continue
                
            finally:
                print(f"⏱ Total processing time: {time.time() - start_time:.2f}s")
            
            time.sleep(1)
            
    finally:
        driver.quit()
        print("\n🏁 Test complete")


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

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Job Scraper')
    parser.add_argument('--test', action='store_true',
                       help='Run in test mode with sample URLs')
    parser.add_argument('--urls', nargs='+',
                       help='Specific URLs to test')
    parser.add_argument('--dry-run', action='store_true',
                       help='Run without saving to Firestore')
    
    args = parser.parse_args()
    
    if args.test:
        test_scrape(test_urls=args.urls, dry_run=args.dry_run)
    else:
        if args.dry_run:
            print("⚠️ Dry run only works with --test mode")
        main()
