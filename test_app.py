"""
Test script for the Education Jobs application
"""

import json
import os
from datetime import datetime

def create_sample_data():
    """Create sample job data for testing"""
    sample_jobs = [
        {
            "role": "Director",
            "title": "Director of Student Services",
            "url": "https://www.edjoin.org/Home/DistrictJobPosting/123456",
            "location": "Los Angeles, CA",
            "district": "Los Angeles Unified School District",
            "date_posted": "2024-01-15",
            "scraped_at": datetime.now().isoformat()
        },
        {
            "role": "Assistant Director",
            "title": "Assistant Director of Curriculum",
            "url": "https://www.edjoin.org/Home/DistrictJobPosting/123457",
            "location": "San Francisco, CA",
            "district": "San Francisco Unified School District",
            "date_posted": "2024-01-14",
            "scraped_at": datetime.now().isoformat()
        },
        {
            "role": "Dean",
            "title": "Dean of Students",
            "url": "https://www.edjoin.org/Home/DistrictJobPosting/123458",
            "location": "San Diego, CA",
            "district": "San Diego Unified School District",
            "date_posted": "2024-01-13",
            "scraped_at": datetime.now().isoformat()
        },
        {
            "role": "Principal",
            "title": "Elementary School Principal",
            "url": "https://www.edjoin.org/Home/DistrictJobPosting/123459",
            "location": "Oakland, CA",
            "district": "Oakland Unified School District",
            "date_posted": "2024-01-12",
            "scraped_at": datetime.now().isoformat()
        }
    ]
    
    with open("edjoin_jobs.json", "w", encoding="utf-8") as f:
        json.dump(sample_jobs, f, indent=2, ensure_ascii=False)
    
    print("✅ Sample job data created")

def test_flask_app():
    """Test the Flask application"""
    try:
        from app import app
        print("✅ Flask app imports successfully")
        
        # Test loading jobs
        with app.app_context():
            from app import load_jobs
            jobs = load_jobs()
            print(f"✅ Loaded {len(jobs)} jobs")
        
        return True
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def test_scraper():
    """Test the scraper module"""
    try:
        from edjoin_scraper import EdJoinScraper
        scraper = EdJoinScraper()
        print("✅ Scraper module imports successfully")
        return True
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Education Jobs Application")
    print("=" * 40)
    
    # Create sample data
    create_sample_data()
    
    # Test modules
    test_scraper()
    test_flask_app()
    
    print("\n✅ All tests completed!")
    print("\nTo start the application, run:")
    print("python run.py")

if __name__ == "__main__":
    main()

