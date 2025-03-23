import os
import time
import json
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, StaleElementReferenceException
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
from schema import validate_job_data
import pprint
import re

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

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_cred)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Configure Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

def get_driver():
    return webdriver.Chrome(options=chrome_options)

def parse_sitemap(url):
    """Parse XML sitemap to extract job URLs"""
    job_urls = []
    try:
        response = requests.get(url, timeout=10)
        root = ElementTree.fromstring(response.content)
        
        # Define namespace if present in the XML
        ns = {'ns': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}
        
        # Check for nested sitemaps
        for child in root:
            tag_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            
            if tag_name == 'sitemap':
                loc_element = child.find('.//ns:loc' if ns else './/loc', ns)
                if loc_element is not None and 'job-sitemap' in loc_element.text:
                    job_urls.extend(parse_sitemap(loc_element.text))
            elif tag_name == 'url':
                loc_element = child.find('.//ns:loc' if ns else './/loc', ns)
                if loc_element is not None and '/remote-jobs/' in loc_element.text:
                    job_urls.append(loc_element.text)
        
        return job_urls
    except Exception as e:
        print(f"Error parsing sitemap: {e}")
        return []

def check_for_json_data(driver):
    """Try to find and extract any structured JSON data on the page"""
    try:
        # Look for script tags with type="application/ld+json"
        script_elements = driver.find_elements(By.XPATH, "//script[@type='application/ld+json']")
        for script in script_elements:
            try:
                json_content = json.loads(script.get_attribute('innerHTML'))
                if isinstance(json_content, dict) and '@type' in json_content:
                    if json_content['@type'] == 'JobPosting':
                        return json_content
            except (json.JSONDecodeError, StaleElementReferenceException):
                continue
                
        # Look for JSON data in other script tags
        script_elements = driver.find_elements(By.TAG_NAME, "script")
        for script in script_elements:
            try:
                script_text = script.get_attribute('innerHTML')
                # Look for objects that might be job data
                match = re.search(r'window\.jobData\s*=\s*({.*?});', script_text, re.DOTALL)
                if match:
                    return json.loads(match.group(1))
            except (json.JSONDecodeError, StaleElementReferenceException):
                continue
                
        return None
    except Exception as e:
        print(f"Error extracting JSON data: {e}")
        return None

def get_text_safely(driver, selector, wait_time=5):
    """Safely extract text from an element using explicit wait"""
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return element.text.strip()
    except (TimeoutException, NoSuchElementException, StaleElementReferenceException):
        return ""

def get_elements_safely(driver, selector, wait_time=5):
    """Safely get multiple elements using explicit wait"""
    try:
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return driver.find_elements(By.CSS_SELECTOR, selector)
    except (TimeoutException, NoSuchElementException):
        return []

def extract_region(driver):
    """Extract region information as a list of regions"""
    regions = []
    try:
        # Look for list item containing "Region"
        region_items = driver.find_elements(By.XPATH, "//li[contains(@class, 'lis-container__job__sidebar__job-about__list__item') and contains(text(), 'Region')]")
        
        if region_items:
            region_elements = region_items[0].find_elements(By.CSS_SELECTOR, ".box--region")
            for element in region_elements:
                regions.append(element.text.strip())
        
        # Fallback method - direct search for region boxes
        if not regions:
            region_boxes = driver.find_elements(By.CSS_SELECTOR, ".box--region")
            for box in region_boxes:
                regions.append(box.text.strip())
    except Exception as e:
        print(f"Error extracting regions: {e}")
    
    return regions

def extract_salary(driver):
    """Extract salary information"""
    try:
        # Look for list item containing "Salary"
        salary_items = driver.find_elements(By.XPATH, "//li[contains(@class, 'lis-container__job__sidebar__job-about__list__item') and contains(text(), 'Salary')]")
        
        if salary_items:
            salary_box = salary_items[0].find_element(By.CSS_SELECTOR, ".box--blue")
            if salary_box:
                return salary_box.text.strip()
        
        # Fallback method - look for salary in other places
        salary_xpath = "//li[contains(text(), 'Salary')]//span[contains(@class, 'box--blue')]"
        salary_elements = driver.find_elements(By.XPATH, salary_xpath)
        if salary_elements:
            return salary_elements[0].text.strip()
            
    except Exception as e:
        print(f"Error extracting salary: {e}")
    
    return ""  # Return empty string if no salary found

def extract_countries(driver):
    """Extract countries from the job listing"""
    countries = []
    try:
        # Look for list item containing "Country"
        country_items = driver.find_elements(By.XPATH, "//li[contains(@class, 'lis-container__job__sidebar__job-about__list__item') and contains(text(), 'Country')]")
        
        if country_items:
            country_boxes = country_items[0].find_elements(By.CSS_SELECTOR, ".box--blue")
            for box in country_boxes:
                countries.append(box.text.strip())
        
        # If no countries found with the above method, try alternative approach
        if not countries:
            # Try another selector pattern
            country_boxes = driver.find_elements(By.XPATH, "//li[contains(text(), 'Country')]//span[contains(@class, 'box--blue')]")
            for box in country_boxes:
                countries.append(box.text.strip())
    except Exception as e:
        print(f"Error extracting countries: {e}")
    
    return countries

def extract_skills(driver):
    """Extract skills from the job listing"""
    skills = []
    try:
        # Look for list item containing "Skills"
        skill_items = driver.find_elements(By.XPATH, "//li[contains(@class, 'lis-container__job__sidebar__job-about__list__item') and contains(text(), 'Skills')]")
        
        if skill_items:
            skill_boxes = skill_items[0].find_elements(By.CSS_SELECTOR, ".box--blue")
            for box in skill_boxes:
                skills.append(box.text.strip())
                
        # If no skills found with the above method, try alternative approach
        if not skills:
            # Try another selector pattern
            skill_boxes = driver.find_elements(By.XPATH, "//li[contains(text(), 'Skills')]//span[contains(@class, 'box--blue')]")
            for box in skill_boxes:
                skills.append(box.text.strip())
    except Exception as e:
        print(f"Error extracting skills: {e}")
    
    return skills

def extract_timezones(driver):
    """Extract timezones from the job listing"""
    timezones = []
    try:
        # Look for list item containing "Timezones"
        timezone_items = driver.find_elements(By.XPATH, "//li[contains(@class, 'lis-container__job__sidebar__job-about__list__item') and contains(text(), 'Timezones')]")
        
        if timezone_items:
            timezone_boxes = timezone_items[0].find_elements(By.CSS_SELECTOR, ".box--blue")
            for box in timezone_boxes:
                timezones.append(box.text.strip())
                
        # If no timezones found with the above method, try alternative approach
        if not timezones:
            # Try another selector pattern
            timezone_boxes = driver.find_elements(By.XPATH, "//li[contains(text(), 'Timezones')]//span[contains(@class, 'box--blue')]")
            for box in timezone_boxes:
                timezones.append(box.text.strip())
    except Exception as e:
        print(f"Error extracting timezones: {e}")
    
    return timezones

def extract_job_data(url, driver):
    """Extract job data using Selenium directly instead of BeautifulSoup"""
    try:
        driver.get(url)
        
        # Wait for the job listing to load
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'listing-header-container'))
            )
        except TimeoutException:
            print(f"Timeout waiting for page to load: {url}")
            # Try an alternative selector
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.lis-container'))
            )
        
        # Try to extract structured JSON data first
        json_data = check_for_json_data(driver)
        if json_data and isinstance(json_data, dict):
            # Use the JSON data to build our job object
            print("Found structured JSON data on the page")
            return process_json_job_data(json_data, url, driver)
        
        # Fall back to direct Selenium extraction if no JSON is found
        parsed_url = urlparse(url)
        job_id = parsed_url.path.split('/')[-1]
        
        # Extract category from URL
        category = "All Other Remote Jobs"
        url_parts = parsed_url.path.split('/')
        if len(url_parts) > 2 and url_parts[1] == 'categories':
            raw_category = '-'.join(url_parts[2].split('-')[1:])
            category = raw_category.title().replace('And', 'and')
        
        # Extract main job details using Selenium
        job_data = {
            'job_id': job_id,
            'title': get_text_safely(driver, '.lis-container__header__hero__company-info__title'),
            'company': get_text_safely(driver, '.lis-container__job__sidebar__companyDetails__info__title h3'),
            'company_about': get_text_safely(driver, '.lis-container__header__hero__company-info__description'),
            'job_description': get_text_safely(driver, '.lis-container__job__content__description'),
            'category': get_text_safely(driver, '.lis-container__header__navigation__tab--category') or category,
            
            # Extract region as a list
            'region': extract_region(driver),
            
            # Optional fields with improved extraction
            'salary_range': extract_salary(driver),
            'countries': extract_countries(driver),
            'skills': extract_skills(driver),
            'timezones': extract_timezones(driver),
            
            # Metadata
            'url': url,
            'source': 'WeWorkRemotely',
            'timestamp': firestore.SERVER_TIMESTAMP
        }
        
        # Try to get apply URL from the correct element
        try:
            # Updated selector to match the element structure you provided
            apply_button = driver.find_element(By.CSS_SELECTOR, ".listing-apply-cta__btn #job-cta-alt")
            job_data['apply_url'] = apply_button.get_attribute('href')
        except NoSuchElementException:
            # Fallback to just looking for the ID
            try:
                apply_button = driver.find_element(By.ID, 'job-cta-alt')
                job_data['apply_url'] = apply_button.get_attribute('href')
            except NoSuchElementException:
                job_data['apply_url'] = url
        
        job_data['apply_before'] = get_text_safely(driver, '.lis-container__job__sidebar__job-about__list__item span') or 'Not specified'
        
        return job_data
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        print(f"Error scraping {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error processing {url}: {e}")
        return None

def process_json_job_data(json_data, url, existing_driver=None):
    """Process structured JSON job data if available"""
    parsed_url = urlparse(url)
    job_id = parsed_url.path.split('/')[-1]
    
    # Extract data from JSON format - adjust based on actual structure
    job_data = {
        'job_id': job_id,
        'title': json_data.get('title', ''),
        'company': json_data.get('hiringOrganization', {}).get('name', '') if isinstance(json_data.get('hiringOrganization'), dict) else '',
        'company_about': '',  # Will extract from page later
        'apply_url': '',  # Will extract from page later
        'apply_before': json_data.get('validThrough', 'Not specified'),
        'job_description': json_data.get('description', ''),
        'category': json_data.get('occupationalCategory', 'All Other Remote Jobs'),
        'region': [],  # Will extract from page as a list
        
        # Optional fields that will be extracted from the page
        'salary_range': '',  # Will extract from page later
        'countries': [],
        'skills': [],
        'timezones': [],
        
        # Metadata
        'url': url,
        'source': 'WeWorkRemotely',
        'timestamp': firestore.SERVER_TIMESTAMP
    }
    
    # Since JSON data doesn't reliably contain all information we need,
    # we'll extract additional information from the page
    driver = existing_driver
    need_to_quit_driver = False
    
    try:
        if not driver:
            driver = get_driver()
            need_to_quit_driver = True
            driver.get(url)
            # Wait for the job information to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.lis-container'))
            )
        
        # Extract additional information from the page
        job_data['company_about'] = get_text_safely(driver, '.lis-container__header__hero__company-info__description')
        job_data['region'] = extract_region(driver)
        job_data['salary_range'] = extract_salary(driver)
        job_data['countries'] = extract_countries(driver)
        job_data['skills'] = extract_skills(driver)
        job_data['timezones'] = extract_timezones(driver)
        
        # Extract apply URL from the correct element
        try:
            # Updated selector to match the element structure you provided
            apply_button = driver.find_element(By.CSS_SELECTOR, ".listing-apply-cta__btn #job-cta-alt")
            job_data['apply_url'] = apply_button.get_attribute('href')
        except NoSuchElementException:
            # Fallback to just looking for the ID
            try:
                apply_button = driver.find_element(By.ID, 'job-cta-alt')
                job_data['apply_url'] = apply_button.get_attribute('href')
            except NoSuchElementException:
                job_data['apply_url'] = url
        
    except Exception as e:
        print(f"Error extracting additional info: {e}")
    finally:
        if driver and need_to_quit_driver:
            driver.quit()
    
    return job_data

def exists_in_firestore(job_id):
    """Check if a job with this ID already exists in Firestore"""
    try:
        doc_ref = db.collection('jobs').document(job_id)
        return doc_ref.get().exists
    except Exception as e:
        print(f"Error checking job existence: {e}")
        # In case of error, return False to allow scraping attempt
        return False

def save_to_firestore(job_data, dry_run=False):
    """Save job data to Firestore, avoiding duplicates"""
    try:
        doc_id = job_data['job_id']
        
        if dry_run:
            print("🚨 Dry Run: Would NOT save to Firestore:")
            pprint.pprint(job_data, indent=2)
            return True
        
        # Document existence should already be checked before this function is called
        # but we'll double-check to be safe
        doc_ref = db.collection('jobs').document(doc_id)
        if not doc_ref.get().exists:
            doc_ref.set(job_data)
            print(f"Saved new job: {doc_id}")
            return True
        else:
            print(f"Job already exists: {doc_id}")
            return False
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
            
            # Initialize start_time before the try block
            start_time = time.time()
            
            try:
                # Extract job_id from URL first
                parsed_url = urlparse(url)
                job_id = parsed_url.path.split('/')[-1]
                print(f"Job ID: {job_id}")
                
                # Check if job already exists in database to avoid unnecessary processing
                if not dry_run and exists_in_firestore(job_id):
                    print(f"⏩ Skipping - Job {job_id} already exists in database")
                    continue
                
                # Extraction
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
                elapsed_time = time.time() - start_time
                print(f"⏱ Total processing time: {elapsed_time:.2f}s")
            
            # Add a small delay between requests
            time.sleep(1)
            
    finally:
        driver.quit()
        print("\n🏁 Test complete")

def main():
    """Main function to scrape all job listings"""
    driver = get_driver()
    
    try:
        sitemap_url = "https://weworkremotely.com/sitemap.xml"
        job_urls = parse_sitemap(sitemap_url)
        print(f"Found {len(job_urls)} job URLs")
        
        # Track progress
        successful = 0
        failed = 0
        skipped = 0
        
        for i, url in enumerate(job_urls, 1):
            print(f"\nProcessing URL {i}/{len(job_urls)}: {url}")
            
            # Initialize start_time at the beginning of each iteration
            start_time = time.time()
            
            try:
                # Extract job_id from URL first
                parsed_url = urlparse(url)
                job_id = parsed_url.path.split('/')[-1]
                
                # Check if job already exists in database
                if exists_in_firestore(job_id):
                    print(f"⏩ Skipping - Job {job_id} already exists in database")
                    skipped += 1
                    # Calculate time even for skipped jobs
                    elapsed_time = time.time() - start_time
                    print(f"⏱ Skipping time: {elapsed_time:.2f}s")
                    continue
                    
                # Process the job only if it doesn't exist
                raw_data = extract_job_data(url, driver)
                if raw_data:
                    try:
                        validated_data = validate_job_data(raw_data)
                        if save_to_firestore(validated_data):
                            successful += 1
                        else:
                            # This should rarely happen since we check existence first
                            skipped += 1
                    except ValueError as e:
                        print(f"Skipping invalid job data: {e}")
                        failed += 1
                    except Exception as e:
                        print(f"Unexpected error validating data: {e}")
                        failed += 1
                else:
                    failed += 1
                    
            except Exception as e:
                print(f"Error processing {url}: {e}")
                failed += 1
                
            finally:
                # Calculate and print elapsed time for all jobs
                elapsed_time = time.time() - start_time
                print(f"⏱ Total processing time: {elapsed_time:.2f}s")
                
            # Add a small delay between requests to be respectful
            time.sleep(3)
            
            # Periodic status update
            if i % 10 == 0:
                print(f"\n--- Progress: {i}/{len(job_urls)} URLs processed. Success: {successful}, Failed: {failed}, Skipped: {skipped} ---\n")
                
    finally:
        driver.quit()
        print(f"\nScraping completed. Processed {len(job_urls)} URLs. Success: {successful}, Failed: {failed}, Skipped: {skipped}")

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
