#!/usr/bin/env python3
"""
Script to check DigitalOcean app deployment status
"""
import subprocess
import time
import json

def run_command(cmd):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}\n{e.stderr}")
        return None

def check_app_status(app_id):
    """Check the status of a DigitalOcean app"""
    cmd = f"doctl apps get {app_id}"
    output = run_command(cmd)
    if output:
        lines = output.split('\n')
        for line in lines:
            if 'Default Ingress' in line:
                ingress = line.split()[-1]
                return ingress
    return None

def main():
    app_id = "be75a943-713e-4252-97fc-14205b3f7837"
    
    print("🔍 Monitoring DigitalOcean App Deployment")
    print("=" * 50)
    print(f"App ID: {app_id}")
    print("Checking deployment status...")
    
    max_attempts = 30  # 5 minutes max
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        print(f"\nAttempt {attempt}/{max_attempts}")
        
        # Check app status
        cmd = f"doctl apps get {app_id}"
        output = run_command(cmd)
        
        if output:
            print("App Status:")
            print(output)
            
            # Check if we have an ingress URL
            if "ondigitalocean.app" in output:
                print("\n🎉 App is live!")
                # Extract the URL
                lines = output.split('\n')
                for line in lines:
                    if 'ondigitalocean.app' in line:
                        url = line.split()[-1]
                        print(f"🌐 URL: https://{url}")
                        print(f"🔗 Test it: https://{url}")
                        return
        
        print("⏳ Still building... waiting 10 seconds")
        time.sleep(10)
    
    print("\n❌ Deployment timed out after 5 minutes")
    print("Check your DigitalOcean dashboard for more details")

if __name__ == "__main__":
    main()
