"""
Deployment Setup Script
Helps configure Google Forms integration and external access
"""

import os
import json
from google_forms_integration import GoogleFormsSubmitter, create_google_form_template

def setup_google_forms():
    """Guide user through Google Forms setup"""
    print("🔧 Google Forms Setup")
    print("=" * 40)
    
    # Show form template
    create_google_form_template()
    
    print("\n📋 Next Steps:")
    print("1. Create a Google Form with the fields above")
    print("2. Get the form submission URL")
    print("3. Get the entry IDs for each field")
    print("4. Update google_forms_integration.py with your URLs and entry IDs")
    
    # Get form URL from user
    form_url = input("\nEnter your Google Form submission URL (or press Enter to skip): ").strip()
    
    if form_url:
        # Update the environment
        os.environ['GOOGLE_FORMS_URL'] = form_url
        print(f"✅ Set GOOGLE_FORMS_URL to: {form_url}")
        
        # Test the URL
        submitter = GoogleFormsSubmitter()
        submitter.forms_url = form_url
        print("✅ Google Forms URL configured")
    else:
        print("⚠️ Skipping Google Forms setup - you can configure this later")

def setup_external_access():
    """Guide user through external access setup"""
    print("\n🌐 External Access Setup")
    print("=" * 40)
    
    print("Choose your deployment option:")
    print("1. Heroku (Free, Easy)")
    print("2. DigitalOcean App Platform")
    print("3. VPS/Server")
    print("4. Skip for now")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        setup_heroku()
    elif choice == "2":
        setup_digitalocean()
    elif choice == "3":
        setup_vps()
    else:
        print("⚠️ Skipping external access setup")

def setup_heroku():
    """Setup Heroku deployment"""
    print("\n🚀 Heroku Setup")
    print("=" * 20)
    
    print("Run these commands:")
    print("1. heroku login")
    print("2. heroku create your-app-name")
    print("3. heroku config:set GOOGLE_FORMS_URL='your-form-url'")
    print("4. heroku config:set FLASK_SECRET_KEY='your-secret-key'")
    print("5. git init")
    print("6. git add .")
    print("7. git commit -m 'Initial commit'")
    print("8. git push heroku main")
    
    app_name = input("\nEnter your Heroku app name (or press Enter to skip): ").strip()
    if app_name:
        print(f"✅ Your app will be available at: https://{app_name}.herokuapp.com")

def setup_digitalocean():
    """Setup DigitalOcean deployment"""
    print("\n🌊 DigitalOcean Setup")
    print("=" * 25)
    
    print("1. Go to DigitalOcean App Platform")
    print("2. Connect your GitHub repository")
    print("3. Set environment variables:")
    print("   - GOOGLE_FORMS_URL")
    print("   - FLASK_SECRET_KEY")
    print("4. Deploy automatically")

def setup_vps():
    """Setup VPS deployment"""
    print("\n🖥️ VPS Setup")
    print("=" * 15)
    
    print("1. Install Python 3 and pip")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Set environment variables")
    print("4. Run with Gunicorn: gunicorn -w 4 -b 0.0.0.0:5000 app:app")
    print("5. Set up Nginx reverse proxy")
    print("6. Configure SSL certificate")

def create_env_file():
    """Create .env file with configuration"""
    print("\n📝 Creating .env file")
    print("=" * 25)
    
    env_content = """# Google Forms Integration
GOOGLE_FORMS_URL=https://docs.google.com/forms/d/YOUR_FORM_ID/formResponse

# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-change-this
FLASK_DEBUG=True

# Domain Configuration (update when deployed)
DOMAIN=http://localhost:5000

# Google Sheets (Optional)
GOOGLE_SHEET_NAME=EdJoin Education Jobs
SERVICE_ACCOUNT_FILE=service_account.json
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file")
    print("📝 Please update the values in .env with your actual configuration")

def create_procfile():
    """Create Procfile for Heroku"""
    print("\n📄 Creating Procfile")
    print("=" * 20)
    
    with open('Procfile', 'w') as f:
        f.write('web: gunicorn app:app\n')
    
    print("✅ Created Procfile for Heroku deployment")

def test_configuration():
    """Test the current configuration"""
    print("\n🧪 Testing Configuration")
    print("=" * 30)
    
    # Test imports
    try:
        from app import app
        print("✅ Flask app imports successfully")
    except Exception as e:
        print(f"❌ Flask app import failed: {e}")
    
    # Test Google Forms integration
    try:
        from google_forms_integration import GoogleFormsSubmitter
        print("✅ Google Forms integration imports successfully")
    except Exception as e:
        print(f"❌ Google Forms integration import failed: {e}")
    
    # Test candidate matching
    try:
        from candidate_matching import CandidateMatcher
        print("✅ Candidate matching imports successfully")
    except Exception as e:
        print(f"❌ Candidate matching import failed: {e}")

def main():
    """Main setup function"""
    print("🚀 Education Jobs Tool - Deployment Setup")
    print("=" * 50)
    
    # Setup Google Forms
    setup_google_forms()
    
    # Setup external access
    setup_external_access()
    
    # Create configuration files
    create_env_file()
    create_procfile()
    
    # Test configuration
    test_configuration()
    
    print("\n🎉 Setup Complete!")
    print("=" * 20)
    print("Next steps:")
    print("1. Update .env file with your actual values")
    print("2. Configure Google Forms integration")
    print("3. Deploy to your chosen platform")
    print("4. Test external access")
    print("5. Integrate with Squarespace")
    
    print("\n📚 For detailed instructions, see DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main()

