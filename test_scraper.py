"""
Test script to demonstrate multi-page scraping from EdJoin.org
"""

from edjoin_scraper import EdJoinScraper
import json

def test_scraper():
    """Test the scraper with different page limits"""
    scraper = EdJoinScraper()
    
    print("🧪 Testing EdJoin.org Multi-Page Scraping")
    print("=" * 50)
    
    # Test with different page limits
    test_cases = [
        {"role": "director", "max_pages": 3},
        {"role": "assistant director", "max_pages": 2},
        {"role": "dean", "max_pages": 2}
    ]
    
    all_jobs = []
    
    for test_case in test_cases:
        print(f"\n🔍 Testing '{test_case['role']}' with {test_case['max_pages']} pages...")
        jobs = scraper.scrape_jobs(test_case['role'], max_pages=test_case['max_pages'])
        all_jobs.extend(jobs)
        print(f"✅ Found {len(jobs)} jobs for '{test_case['role']}'")
    
    print(f"\n📊 Total jobs found: {len(all_jobs)}")
    
    # Show sample jobs
    if all_jobs:
        print("\n📋 Sample jobs found:")
        for i, job in enumerate(all_jobs[:5], 1):
            print(f"{i}. {job['title']} ({job['role']}) - {job.get('location', 'Location not specified')}")
    
    # Save results
    with open('test_scraper_results.json', 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to 'test_scraper_results.json'")
    
    return all_jobs

if __name__ == "__main__":
    test_scraper()

