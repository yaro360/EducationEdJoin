"""
Google Forms Integration for Candidate Data
Automatically submits candidate registrations to Google Forms
"""

import requests
import json
from datetime import datetime
import os

class GoogleFormsSubmitter:
    def __init__(self):
        # Google Forms submission URL (you'll get this from your Google Form)
        self.forms_url = os.environ.get('GOOGLE_FORMS_URL', '')
        
        # Form field mapping
        self.field_mapping = {
            'entry.1234567890': 'name',           # Replace with actual entry IDs
            'entry.1234567891': 'email',           # Replace with actual entry IDs
            'entry.1234567892': 'phone',           # Replace with actual entry IDs
            'entry.1234567893': 'years_experience', # Replace with actual entry IDs
            'entry.1234567894': 'education_level', # Replace with actual entry IDs
            'entry.1234567895': 'preferred_roles', # Replace with actual entry IDs
            'entry.1234567896': 'preferred_locations', # Replace with actual entry IDs
            'entry.1234567897': 'skills',          # Replace with actual entry IDs
            'entry.1234567898': 'resume_url',      # Replace with actual entry IDs
            'entry.1234567899': 'timestamp'        # Replace with actual entry IDs
        }
    
    def submit_to_google_forms(self, candidate_data):
        """Submit candidate data to Google Forms"""
        if not self.forms_url:
            print("⚠️ Google Forms URL not configured")
            return False
        
        try:
            # Prepare form data
            form_data = {}
            for entry_id, field_name in self.field_mapping.items():
                if field_name in candidate_data:
                    value = candidate_data[field_name]
                    
                    # Handle different data types
                    if isinstance(value, list):
                        value = ', '.join(value)
                    elif isinstance(value, int):
                        value = str(value)
                    
                    form_data[entry_id] = value
            
            # Add timestamp
            timestamp_entry = 'entry.1234567899'  # Replace with actual timestamp entry ID
            form_data[timestamp_entry] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Submit to Google Forms
            response = requests.post(self.forms_url, data=form_data, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Successfully submitted candidate {candidate_data.get('name')} to Google Forms")
                return True
            else:
                print(f"❌ Failed to submit to Google Forms: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error submitting to Google Forms: {e}")
            return False
    
    def get_form_entry_ids(self, google_form_url):
        """Instructions to get Google Form entry IDs"""
        instructions = """
        📋 How to Get Google Form Entry IDs:
        
        1. Open your Google Form in edit mode
        2. Right-click on each field and select "Inspect Element"
        3. Look for the 'name' attribute in the HTML
        4. The name will be something like 'entry.1234567890'
        5. Copy these entry IDs and update the field_mapping in this file
        
        Example:
        - Name field: entry.1234567890
        - Email field: entry.1234567891
        - Phone field: entry.1234567892
        - etc.
        
        Then update the field_mapping dictionary with the correct entry IDs.
        """
        print(instructions)
        return instructions

def create_google_form_template():
    """Create a sample Google Form structure"""
    form_structure = {
        "title": "Education Leadership Candidate Registration",
        "description": "This form captures candidate information for education leadership positions",
        "fields": [
            {
                "title": "Full Name",
                "type": "short_answer",
                "required": True,
                "description": "Candidate's full name"
            },
            {
                "title": "Email Address", 
                "type": "short_answer",
                "required": True,
                "description": "Primary email address"
            },
            {
                "title": "Phone Number",
                "type": "short_answer", 
                "required": False,
                "description": "Contact phone number"
            },
            {
                "title": "Years of Experience",
                "type": "multiple_choice",
                "required": True,
                "options": ["0-1 years", "2-3 years", "4-5 years", "6-8 years", "9-12 years", "13+ years"]
            },
            {
                "title": "Education Level",
                "type": "multiple_choice",
                "required": True,
                "options": ["Bachelor's Degree", "Master's Degree", "Master of Education", "PhD/Doctorate", "EdD"]
            },
            {
                "title": "Preferred Roles",
                "type": "checkboxes",
                "required": True,
                "options": ["Director", "Assistant Director", "Dean", "Principal", "Superintendent"]
            },
            {
                "title": "Preferred Locations",
                "type": "short_answer",
                "required": False,
                "description": "Comma-separated list of preferred locations"
            },
            {
                "title": "Key Skills",
                "type": "short_answer",
                "required": False,
                "description": "Comma-separated list of key skills"
            },
            {
                "title": "Resume URL",
                "type": "short_answer",
                "required": False,
                "description": "Link to uploaded resume"
            },
            {
                "title": "Registration Timestamp",
                "type": "short_answer",
                "required": False,
                "description": "When the candidate registered"
            }
        ]
    }
    
    print("📝 Google Form Structure:")
    print(json.dumps(form_structure, indent=2))
    return form_structure

if __name__ == "__main__":
    submitter = GoogleFormsSubmitter()
    submitter.get_form_entry_ids("")
    create_google_form_template()
