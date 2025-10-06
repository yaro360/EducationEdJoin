#!/usr/bin/env python3
"""
Test script to verify deployment data loading
"""

import json
import os

def test_data_loading():
    """Test if data is loading correctly"""
    print("🔍 Testing data loading...")
    
    # Check if jobs file exists
    jobs_file = "edjoin_jobs.json"
    if not os.path.exists(jobs_file):
        print(f"❌ {jobs_file} not found")
        return False
    
    # Load and check data
    try:
        with open(jobs_file, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
        
        print(f"✅ Jobs file loaded: {len(jobs)} positions")
        
        if len(jobs) == 0:
            print("❌ No jobs found in file")
            return False
        
        # Show sample data
        print(f"📋 Sample job: {jobs[0]['title']} - {jobs[0]['role']}")
        
        # Check roles
        roles = list(set(job.get('role', 'Unknown') for job in jobs))
        print(f"🎯 Available roles: {roles}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading jobs: {e}")
        return False

def test_app_loading():
    """Test if Flask app loads correctly"""
    print("\n🔍 Testing Flask app loading...")
    
    try:
        from app import app, load_jobs
        
        # Test load_jobs function
        jobs = load_jobs()
        print(f"✅ Flask app loaded: {len(jobs)} positions")
        
        return len(jobs) > 0
        
    except Exception as e:
        print(f"❌ Error loading Flask app: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Education Jobs Deployment")
    print("=" * 50)
    
    data_ok = test_data_loading()
    app_ok = test_app_loading()
    
    if data_ok and app_ok:
        print("\n✅ All tests passed! App should work correctly.")
    else:
        print("\n❌ Some tests failed. Check the issues above.")
