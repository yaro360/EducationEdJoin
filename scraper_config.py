"""
Configuration for EdJoin.org scraper
Easily adjust scraping parameters here
"""

# Scraping Configuration
SCRAPING_CONFIG = {
    # Maximum pages to scrape per role
    "max_pages_per_role": 10,
    
    # Delay between requests (seconds) - be respectful to the server
    "request_delay": 2,
    
    # Target roles to scrape
    "target_roles": [
        "director",
        "assistant director", 
        "dean",
        "principal",
        "superintendent"
    ],
    
    # Additional search terms for each role
    "role_variations": {
        "director": ["director", "director of", "executive director"],
        "assistant director": ["assistant director", "associate director"],
        "dean": ["dean", "dean of", "assistant dean"],
        "principal": ["principal", "head of school", "school leader"],
        "superintendent": ["superintendent", "superintendent of schools"]
    },
    
    # Job posting age limit (days) - only scrape recent postings
    "max_age_days": 30,
    
    # Minimum job title length (filter out very short titles)
    "min_title_length": 10,
    
    # Location filters (optional)
    "preferred_locations": [
        "California",
        "Los Angeles",
        "San Francisco", 
        "San Diego",
        "Oakland"
    ]
}

# Advanced Configuration
ADVANCED_CONFIG = {
    # Retry failed requests
    "max_retries": 3,
    
    # Request timeout
    "request_timeout": 10,
    
    # User agent rotation
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ],
    
    # Enable/disable features
    "features": {
        "extract_salary": True,
        "extract_requirements": True,
        "extract_description": False,  # Can be slow
        "save_html_debug": False
    }
}

def get_config():
    """Get the current scraping configuration"""
    return SCRAPING_CONFIG

def get_advanced_config():
    """Get advanced configuration options"""
    return ADVANCED_CONFIG

def update_max_pages(max_pages):
    """Update the maximum pages per role"""
    SCRAPING_CONFIG["max_pages_per_role"] = max_pages
    print(f"✅ Updated max pages per role to: {max_pages}")

def add_role(role):
    """Add a new role to scrape"""
    if role not in SCRAPING_CONFIG["target_roles"]:
        SCRAPING_CONFIG["target_roles"].append(role)
        print(f"✅ Added new role: {role}")
    else:
        print(f"⚠️ Role '{role}' already exists")

def remove_role(role):
    """Remove a role from scraping"""
    if role in SCRAPING_CONFIG["target_roles"]:
        SCRAPING_CONFIG["target_roles"].remove(role)
        print(f"✅ Removed role: {role}")
    else:
        print(f"⚠️ Role '{role}' not found")

if __name__ == "__main__":
    print("🔧 EdJoin Scraper Configuration")
    print("=" * 40)
    print(f"Max pages per role: {SCRAPING_CONFIG['max_pages_per_role']}")
    print(f"Target roles: {', '.join(SCRAPING_CONFIG['target_roles'])}")
    print(f"Request delay: {SCRAPING_CONFIG['request_delay']} seconds")
    print(f"Total potential pages: {SCRAPING_CONFIG['max_pages_per_role'] * len(SCRAPING_CONFIG['target_roles'])}")

