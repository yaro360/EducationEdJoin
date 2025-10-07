"""
Automatic Job Refresh System
Refreshes job positions automatically on a schedule
"""

import schedule
import time
import subprocess
import sys
import logging
from datetime import datetime
import os
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_refresh.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class JobRefreshScheduler:
    def __init__(self):
        self.scraper_script = "production_scraper.py"
        self.jobs_file = "edjoin_jobs.json"
        self.last_refresh = None
        
    def run_job_scraper(self):
        """Run the job scraper and update positions"""
        try:
            logging.info("🔄 Starting scheduled job refresh...")
            
            # Run the production scraper
            result = subprocess.run(
                [sys.executable, self.scraper_script], 
                capture_output=True, 
                text=True, 
                timeout=1800  # 30 minute timeout
            )
            
            if result.returncode == 0:
                # Count new positions
                try:
                    with open(self.jobs_file, 'r', encoding='utf-8') as f:
                        jobs = json.load(f)
                    position_count = len(jobs)
                    
                    logging.info(f"✅ Job refresh completed successfully!")
                    logging.info(f"📊 Found {position_count} total positions")
                    
                    # Log position breakdown
                    role_counts = {}
                    for job in jobs:
                        role = job.get('role', 'Unknown')
                        role_counts[role] = role_counts.get(role, 0) + 1
                    
                    for role, count in role_counts.items():
                        logging.info(f"   {role}: {count} positions")
                    
                    self.last_refresh = datetime.now().isoformat()
                    
                    # Send notification (optional)
                    self.send_refresh_notification(position_count, role_counts)
                    
                except Exception as e:
                    logging.error(f"Error reading updated jobs file: {e}")
                    
            else:
                logging.error(f"❌ Job scraper failed with return code {result.returncode}")
                logging.error(f"Error output: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            logging.error("⏰ Job scraper timed out after 30 minutes")
        except Exception as e:
            logging.error(f"❌ Error running job scraper: {e}")
    
    def send_refresh_notification(self, position_count, role_counts):
        """Send notification about refresh results (optional)"""
        try:
            # You can add email notifications here
            # For now, just log the summary
            logging.info("📧 Refresh notification:")
            logging.info(f"   Total positions: {position_count}")
            logging.info(f"   Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            logging.error(f"Error sending notification: {e}")
    
    def setup_schedule(self):
        """Set up the scheduling system"""
        logging.info("⏰ Setting up job refresh schedule...")
        
        # Schedule job refresh every 24 hours at 6 AM
        schedule.every().day.at("06:00").do(self.run_job_scraper)
        
        # Alternative schedules (uncomment to use):
        # schedule.every(12).hours.do(self.run_job_scraper)  # Every 12 hours
        # schedule.every().hour.do(self.run_job_scraper)     # Every hour
        # schedule.every(30).minutes.do(self.run_job_scraper) # Every 30 minutes
        
        # Weekly schedule (uncomment to use):
        # schedule.every().monday.at("06:00").do(self.run_job_scraper)  # Every Monday
        # schedule.every().wednesday.at("06:00").do(self.run_job_scraper)  # Every Wednesday
        # schedule.every().friday.at("06:00").do(self.run_job_scraper)  # Every Friday
        
        logging.info("✅ Schedule configured:")
        logging.info("   - Daily at 06:00 AM")
        logging.info("   - 30-minute timeout per run")
        logging.info("   - Automatic error handling")
    
    def run_scheduler(self):
        """Run the scheduler continuously"""
        logging.info("🚀 Starting job refresh scheduler...")
        logging.info("Press Ctrl+C to stop")
        
        # Run initial refresh
        logging.info("🔄 Running initial job refresh...")
        self.run_job_scraper()
        
        # Keep scheduler running
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logging.info("👋 Scheduler stopped by user")
                break
            except Exception as e:
                logging.error(f"Error in scheduler loop: {e}")
                time.sleep(60)

def create_cron_job():
    """Create a cron job for automatic scheduling"""
    cron_script = """#!/bin/bash
# Education Jobs Auto-Refresh Cron Job
# Runs every day at 6 AM

cd /Users/yco/Desktop/JobSourcingRosa
python3 production_scraper.py >> job_refresh.log 2>&1
"""
    
    with open('run_job_refresh.sh', 'w') as f:
        f.write(cron_script)
    
    os.chmod('run_job_refresh.sh', 0o755)
    
    print("📝 Created cron job script: run_job_refresh.sh")
    print("To set up cron job, run:")
    print("crontab -e")
    print("Then add this line:")
    print("0 6 * * * /Users/yco/Desktop/JobSourcingRosa/run_job_refresh.sh")

def create_systemd_service():
    """Create a systemd service for Linux systems"""
    service_content = """[Unit]
Description=Education Jobs Auto-Refresh Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/JobSourcingRosa
ExecStart=/usr/bin/python3 /path/to/JobSourcingRosa/auto_refresh_system.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    with open('education-jobs-refresh.service', 'w') as f:
        f.write(service_content)
    
    print("📝 Created systemd service file: education-jobs-refresh.service")
    print("To install:")
    print("sudo cp education-jobs-refresh.service /etc/systemd/system/")
    print("sudo systemctl enable education-jobs-refresh")
    print("sudo systemctl start education-jobs-refresh")

def main():
    """Main function"""
    print("🔄 Education Jobs Auto-Refresh System")
    print("=" * 50)
    
    scheduler = JobRefreshScheduler()
    
    print("Choose your scheduling method:")
    print("1. Python scheduler (runs continuously)")
    print("2. Cron job (system-level scheduling)")
    print("3. Systemd service (Linux)")
    print("4. Manual refresh only")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        scheduler.setup_schedule()
        scheduler.run_scheduler()
    elif choice == "2":
        create_cron_job()
    elif choice == "3":
        create_systemd_service()
    elif choice == "4":
        print("🔄 Running manual refresh...")
        scheduler.run_job_scraper()
    else:
        print("Invalid choice. Running manual refresh...")
        scheduler.run_job_scraper()

if __name__ == "__main__":
    main()

