#!/usr/bin/env python3
"""
Create Optimized DigitalOcean App
Creates a new app with single component to reduce costs to $24/month
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

def create_optimized_app():
    """Create a new optimized app with single component"""
    print("🚀 Creating Optimized DigitalOcean App")
    print("=" * 40)
    print("This will create a new app with:")
    print("✅ Single component (reduces cost to $24/month)")
    print("✅ Basic XXS instance (cheapest option)")
    print("✅ Connected to your GitHub repo")
    print()
    
    # Create app spec file
    app_spec = """name: education-jobs-optimized
services:
  - name: web
    source_dir: /
    github:
      repo: yaro360/EducationEdJoin
      branch: main
    run_command: gunicorn --bind 0.0.0.0:8080 app:app
    environment_slug: python
    instance_count: 1
    instance_size_slug: basic-xxs
    http_port: 8080
    health_check:
      http_path: /
      initial_delay_seconds: 10
      period_seconds: 10
      timeout_seconds: 5
      success_threshold: 1
      failure_threshold: 3
"""
    
    with open("app-spec-optimized.yaml", "w") as f:
        f.write(app_spec)
    
    print("📝 Created app-spec-optimized.yaml")
    print()
    print("🔧 To create the optimized app:")
    print("1. Go to DigitalOcean Dashboard")
    print("2. Click 'Create App'")
    print("3. Choose 'From Source Code'")
    print("4. Connect GitHub repository: yaro360/EducationEdJoin")
    print("5. Select 'main' branch")
    print("6. Choose 'Web Service'")
    print("7. Set these settings:")
    print("   - Instance Size: Basic XXS ($12/month)")
    print("   - Instance Count: 1")
    print("   - Run Command: gunicorn --bind 0.0.0.0:8080 app:app")
    print("   - HTTP Port: 8080")
    print("8. Deploy the app")
    print()
    print("💰 Expected cost: $12-24/month (much cheaper!)")

def check_current_apps():
    """Check current apps"""
    print("🔍 Current DigitalOcean Apps:")
    print("-" * 30)
    
    success, output, error = run_doctl_command("doctl apps list")
    if success:
        print(output)
    else:
        print(f"Error: {error}")

def main():
    print("🎯 DigitalOcean App Optimization")
    print("=" * 35)
    
    check_current_apps()
    print()
    
    print("💡 Current situation:")
    print("- You have 1 app running at $48/month")
    print("- We'll create a new optimized app at $12-24/month")
    print("- Then you can delete the expensive one")
    print()
    
    choice = input("Create optimized app? (yes/no): ").strip().lower()
    
    if choice in ['yes', 'y']:
        create_optimized_app()
    else:
        print("❌ Operation cancelled")
        print("\n💡 You can manually create a new app in DigitalOcean dashboard")

if __name__ == "__main__":
    main()
