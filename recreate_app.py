#!/usr/bin/env python3
"""
Recreate DigitalOcean App with Single Component
This will delete the current app and recreate it with just one component to reduce costs
"""

import subprocess
import json
import sys

def run_doctl_command(command):
    """Run a doctl command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def delete_current_app():
    """Delete the current app"""
    app_id = "179fb823-46e7-49e7-bfc6-d6f54e969a72"
    
    print(f"🗑️  Deleting current app: {app_id}")
    
    confirm = input("⚠️  Are you sure you want to delete the current app? This will temporarily take your site down! (yes/no): ")
    if confirm.lower() not in ['yes', 'y']:
        print("❌ Deletion cancelled")
        return False
    
    success, output, error = run_doctl_command(f"doctl apps delete {app_id} --force")
    if success:
        print("✅ App deleted successfully")
        return True
    else:
        print(f"❌ Error deleting app: {error}")
        return False

def create_new_app():
    """Create a new app with single component"""
    print("\n🚀 Creating new app with single component...")
    
    # Create app spec
    app_spec = {
        "name": "education-jobs-single",
        "services": [
            {
                "name": "web",
                "source_dir": "/",
                "github": {
                    "repo": "yaro360/EducationEdJoin",
                    "branch": "main"
                },
                "run_command": "gunicorn --bind 0.0.0.0:8080 app:app",
                "environment_slug": "python",
                "instance_count": 1,
                "instance_size_slug": "basic-xxs"
            }
        ]
    }
    
    # Save spec to file
    with open("app-spec.yaml", "w") as f:
        f.write(f"name: education-jobs-single\n")
        f.write(f"services:\n")
        f.write(f"  - name: web\n")
        f.write(f"    source_dir: /\n")
        f.write(f"    github:\n")
        f.write(f"      repo: yaro360/EducationEdJoin\n")
        f.write(f"      branch: main\n")
        f.write(f"    run_command: gunicorn --bind 0.0.0.0:8080 app:app\n")
        f.write(f"    environment_slug: python\n")
        f.write(f"    instance_count: 1\n")
        f.write(f"    instance_size_slug: basic-xxs\n")
    
    print("📝 App spec created: app-spec.yaml")
    print("🔧 To create the new app manually:")
    print("1. Go to DigitalOcean Dashboard")
    print("2. Click 'Create App'")
    print("3. Connect your GitHub repository: yaro360/EducationEdJoin")
    print("4. Select 'main' branch")
    print("5. Choose 'Web Service'")
    print("6. Set instance size to 'Basic XXS' (cheapest)")
    print("7. Deploy the app")

def main():
    print("🔧 DigitalOcean App Recreation Tool")
    print("=" * 40)
    print("This will help you reduce costs by creating a single-component app")
    print()
    
    print("Current situation:")
    print("- You have 1 app with 2 components ($48/month)")
    print("- We'll delete the current app and recreate with 1 component")
    print()
    
    choice = input("Do you want to proceed? (yes/no): ").strip().lower()
    
    if choice in ['yes', 'y']:
        if delete_current_app():
            create_new_app()
    else:
        print("❌ Operation cancelled")
        print("\n💡 Alternative: Check your DigitalOcean dashboard to see what components are running")

if __name__ == "__main__":
    main()

