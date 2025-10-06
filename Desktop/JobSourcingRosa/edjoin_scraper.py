"""
EdJoin.org Job Scraper
Scrapes director-level positions from EdJoin.org and saves to Google Sheets
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
ROLES = ["director", "assistant director", "dean", "principal", "superintendent"]
GOOGLE_SHEET_NAME = "EdJoin Education Jobs"
SERVICE_ACCOUNT_FILE = "service_account.json"

class EdJoinScraper:
    def __init__(self):
        self.base_url = "https://www.edjoin.org"
        self.search_url = f"{self.base_url}/search"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def scrape_jobs(self, keyword, max_pages=10):
        """Scrape jobs for a specific keyword with enhanced error handling"""
        jobs = []
        page = 1
        
        while page <= max_pages:
            print(f"Scraping '{keyword}' - page {page}...")
            
            params = {
                "keywords": keyword,
                "page": page,
                "sort": "date"
            }
            
            try:
                # Add random delay to avoid rate limiting
                time.sleep(random.uniform(1, 3))
                
                response = self.session.get(self.search_url, params=params, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for job listings with multiple selectors
                    job_cards = soup.find_all("div", class_=["job-info", "job-listing", "search-result", "result-item"])
                    
                    if not job_cards:
                        # Try alternative selectors
                        job_cards = soup.find_all("div", class_="card")
                        if not job_cards:
                            job_cards = soup.find_all("article")
                    
                    if not job_cards:
                        print(f"No more jobs found for '{keyword}' on page {page}")
                        break
                    
                    page_jobs = 0
                    for job in job_cards:
                        job_data = self.extract_job_data(job, keyword)
                        if job_data:
                            jobs.append(job_data)
                            page_jobs += 1
                    
                    if page_jobs == 0:
                        print(f"No valid jobs found for '{keyword}' on page {page}")
                        break
                    
                    print(f"Found {page_jobs} jobs on page {page}")
                    page += 1
                    
                elif response.status_code == 500:
                    print(f"⚠️ EdJoin.org returned 500 error for '{keyword}' - server may be down")
                    break
                else:
                    print(f"Error: HTTP {response.status_code} for '{keyword}' page {page}")
                    break
                    
            except requests.RequestException as e:
                print(f"Network error for '{keyword}' page {page}: {e}")
                break
            except Exception as e:
                print(f"Unexpected error for '{keyword}' page {page}: {e}")
                break
                
        return jobs
    
    def extract_job_data(self, job_element, role_keyword):
        """Extract job data from a job element"""
        try:
            # Try different selectors for job title and link
            title_elem = job_element.find("a", class_=["job-title", "title", "position-title"])
            if not title_elem:
                title_elem = job_element.find("h3")
            if not title_elem:
                title_elem = job_element.find("h4")
            
            if not title_elem:
                return None
                
            title = title_elem.get_text(strip=True)
            if not title:
                return None
                
            # Get job URL
            href = title_elem.get('href', '')
            if href.startswith('/'):
                url = f"{self.base_url}{href}"
            elif href.startswith('http'):
                url = href
            else:
                url = f"{self.base_url}/{href}"
            
            # Extract additional info if available
            location = ""
            district = ""
            date_posted = ""
            
            # Try to find location
            location_elem = job_element.find("span", class_=["location", "city", "district"])
            if location_elem:
                location = location_elem.get_text(strip=True)
            
            # Try to find district
            district_elem = job_element.find("div", class_=["district", "employer"])
            if district_elem:
                district = district_elem.get_text(strip=True)
            
            # Try to find date
            date_elem = job_element.find("span", class_=["date", "posted"])
            if date_elem:
                date_posted = date_elem.get_text(strip=True)
            
            return {
                "role": role_keyword.title(),
                "title": title,
                "url": url,
                "location": location,
                "district": district,
                "date_posted": date_posted,
                "scraped_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error extracting job data: {e}")
            return None
    
    def run_full_scrape(self):
        """Run scraper for all roles"""
        all_jobs = []
        
        for role in ROLES:
            print(f"\n=== Scraping {role.upper()} positions ===")
            jobs = self.scrape_jobs(role)
            all_jobs.extend(jobs)
            print(f"Found {len(jobs)} {role} positions")
        
        print(f"\nTotal jobs found: {len(all_jobs)}")
        return all_jobs
    
    def save_to_json(self, jobs, filename="edjoin_jobs.json"):
        """Save jobs to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(jobs)} jobs to {filename}")
    
    def save_to_google_sheets(self, jobs):
        """Save jobs to Google Sheets"""
        try:
            if not os.path.exists(SERVICE_ACCOUNT_FILE):
                print(f"Service account file {SERVICE_ACCOUNT_FILE} not found. Please add your Google service account credentials.")
                return False
                
            creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
            client = gspread.authorize(creds)
            
            # Try to open existing sheet or create new one
            try:
                sheet = client.open(GOOGLE_SHEET_NAME).sheet1
            except gspread.SpreadsheetNotFound:
                print(f"Creating new Google Sheet: {GOOGLE_SHEET_NAME}")
                sheet = client.create(GOOGLE_SHEET_NAME).sheet1
            
            # Clear existing data and add headers
            sheet.clear()
            headers = ["Role", "Title", "Location", "District", "Date Posted", "URL", "Scraped At"]
            sheet.append_row(headers)
            
            # Add job data
            for job in jobs:
                row = [
                    job.get("role", ""),
                    job.get("title", ""),
                    job.get("location", ""),
                    job.get("district", ""),
                    job.get("date_posted", ""),
                    job.get("url", ""),
                    job.get("scraped_at", "")
                ]
                sheet.append_row(row)
            
            print(f"✅ Uploaded {len(jobs)} jobs to Google Sheet: {GOOGLE_SHEET_NAME}")
            return True
            
        except Exception as e:
            print(f"Error uploading to Google Sheets: {e}")
            return False

def main():
    """Main function to run the scraper"""
    scraper = EdJoinScraper()
    
    print("Starting EdJoin.org job scraping...")
    print(f"Target roles: {', '.join(ROLES)}")
    
    # Run the scraper
    jobs = scraper.run_full_scrape()
    
    if jobs:
        # Save to JSON
        scraper.save_to_json(jobs)
        
        # Save to Google Sheets
        scraper.save_to_google_sheets(jobs)
        
        print(f"\n✅ Scraping completed! Found {len(jobs)} total positions.")
    else:
        print("❌ No jobs found. The website structure may have changed.")

if __name__ == "__main__":
    main()
