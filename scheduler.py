"""
Automated scheduler for running the EdJoin scraper
"""

import schedule
import time
import subprocess
import sys
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_scraper():
    """Run the EdJoin scraper"""
    try:
        logging.info("Starting scheduled scraper run...")
        result = subprocess.run([sys.executable, 'edjoin_scraper.py'], 
                              capture_output=True, text=True, timeout=1800)  # 30 min timeout
        
        if result.returncode == 0:
            logging.info("Scraper completed successfully")
            logging.info(f"Output: {result.stdout}")
        else:
            logging.error(f"Scraper failed with return code {result.returncode}")
            logging.error(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        logging.error("Scraper timed out after 30 minutes")
    except Exception as e:
        logging.error(f"Error running scraper: {e}")

def main():
    """Main scheduler function"""
    logging.info("Starting job scheduler...")
    
    # Schedule jobs
    schedule.every().day.at("06:00").do(run_scraper)  # Daily at 6 AM
    schedule.every().day.at("18:00").do(run_scraper)  # Daily at 6 PM
    
    # Optional: Run immediately on startup for testing
    # run_scraper()
    
    logging.info("Scheduler started. Jobs scheduled:")
    logging.info("- Daily at 06:00")
    logging.info("- Daily at 18:00")
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()

