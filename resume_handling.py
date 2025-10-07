"""
Resume Handling Solutions
Multiple approaches for handling candidate resume uploads
"""

import os
import json
import requests
from datetime import datetime
import uuid
from google_forms_integration import GoogleFormsSubmitter

class ResumeHandler:
    def __init__(self):
        self.upload_folder = "uploads"
        self.base_url = os.environ.get('DOMAIN', 'http://localhost:5000')
        
    def save_resume(self, file, candidate_id):
        """Save uploaded resume file"""
        if file and file.filename:
            # Generate unique filename
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{candidate_id}_{uuid.uuid4()}.{file_extension}"
            
            # Save file
            file_path = os.path.join(self.upload_folder, filename)
            file.save(file_path)
            
            # Return public URL
            resume_url = f"{self.base_url}/uploads/{filename}"
            return resume_url, filename
        
        return None, None
    
    def get_resume_url(self, filename):
        """Get public URL for resume file"""
        if filename:
            return f"{self.base_url}/uploads/{filename}"
        return None

class GoogleDriveUploader:
    """Upload resumes to Google Drive and get shareable links"""
    
    def __init__(self):
        self.service_account_file = "service_account.json"
        self.drive_folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID', '')
    
    def upload_to_drive(self, file_path, candidate_name):
        """Upload resume to Google Drive"""
        try:
            from google.oauth2.service_account import Credentials
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            
            # Authenticate
            creds = Credentials.from_service_account_file(self.service_account_file)
            service = build('drive', 'v3', credentials=creds)
            
            # Create file metadata
            file_metadata = {
                'name': f"{candidate_name}_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                'parents': [self.drive_folder_id] if self.drive_folder_id else []
            }
            
            # Upload file
            media = MediaFileUpload(file_path, mimetype='application/pdf')
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,webViewLink'
            ).execute()
            
            # Make file publicly viewable
            service.permissions().create(
                fileId=file['id'],
                body={'role': 'reader', 'type': 'anyone'}
            ).execute()
            
            return file['webViewLink']
            
        except Exception as e:
            print(f"Error uploading to Google Drive: {e}")
            return None

class EmailResumeHandler:
    """Send resumes via email to Google Forms or directly"""
    
    def __init__(self):
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.email_user = os.environ.get('EMAIL_USER', '')
        self.email_password = os.environ.get('EMAIL_PASSWORD', '')
        self.admin_email = os.environ.get('ADMIN_EMAIL', '')
    
    def send_resume_email(self, candidate_data, resume_path):
        """Send resume via email"""
        try:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.base import MIMEBase
            from email import encoders
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = self.admin_email
            msg['Subject'] = f"New Candidate Registration: {candidate_data.get('name')}"
            
            # Email body
            body = f"""
            New candidate registration received:
            
            Name: {candidate_data.get('name')}
            Email: {candidate_data.get('email')}
            Phone: {candidate_data.get('phone', 'Not provided')}
            Experience: {candidate_data.get('years_experience')} years
            Education: {candidate_data.get('education_level')}
            Preferred Roles: {', '.join(candidate_data.get('preferred_roles', []))}
            Preferred Locations: {', '.join(candidate_data.get('preferred_locations', []))}
            Skills: {', '.join(candidate_data.get('skills', []))}
            
            Resume attached.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach resume
            if resume_path and os.path.exists(resume_path):
                with open(resume_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(resume_path)}'
                )
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            text = msg.as_string()
            server.sendmail(self.email_user, self.admin_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

class GoogleFormsWithResume:
    """Enhanced Google Forms integration with resume handling"""
    
    def __init__(self):
        self.google_forms_submitter = GoogleFormsSubmitter()
        self.resume_handler = ResumeHandler()
        self.drive_uploader = GoogleDriveUploader()
        self.email_handler = EmailResumeHandler()
    
    def submit_candidate_with_resume(self, candidate_data, resume_file=None):
        """Submit candidate data to Google Forms with resume handling"""
        
        # Handle resume upload
        resume_url = None
        resume_filename = None
        
        if resume_file:
            # Option 1: Save locally and include URL in Google Form
            resume_url, resume_filename = self.resume_handler.save_resume(
                resume_file, candidate_data.get('id', 'unknown')
            )
            
            # Option 2: Upload to Google Drive (if configured)
            if self.drive_uploader.drive_folder_id:
                drive_url = self.drive_uploader.upload_to_drive(
                    f"uploads/{resume_filename}", 
                    candidate_data.get('name', 'Candidate')
                )
                if drive_url:
                    resume_url = drive_url
        
        # Add resume URL to candidate data
        candidate_data['resume_url'] = resume_url
        candidate_data['resume_filename'] = resume_filename
        
        # Submit to Google Forms
        success = self.google_forms_submitter.submit_to_google_forms(candidate_data)
        
        # Option 3: Send email with resume attachment
        if resume_filename and self.email_handler.admin_email:
            self.email_handler.send_resume_email(
                candidate_data, 
                f"uploads/{resume_filename}"
            )
        
        return success, resume_url

def create_resume_upload_route(app):
    """Add resume upload route to Flask app"""
    
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        """Serve uploaded resume files"""
        from flask import send_from_directory
        return send_from_directory('uploads', filename)
    
    return app

# Configuration options
RESUME_HANDLING_OPTIONS = {
    "option_1": {
        "name": "Local Storage + Google Forms URL",
        "description": "Save resumes locally, include download URL in Google Form",
        "pros": ["Simple", "No additional setup", "Works immediately"],
        "cons": ["Requires server storage", "URLs may change"]
    },
    "option_2": {
        "name": "Google Drive Integration",
        "description": "Upload resumes to Google Drive, share public links",
        "pros": ["Professional", "Reliable URLs", "Easy access"],
        "cons": ["Requires Google Drive API setup", "More complex"]
    },
    "option_3": {
        "name": "Email with Attachments",
        "description": "Send resumes via email to admin",
        "pros": ["Direct delivery", "No storage needed", "Immediate notification"],
        "cons": ["Email size limits", "Requires email setup"]
    },
    "option_4": {
        "name": "Hybrid Approach",
        "description": "Combine multiple methods for reliability",
        "pros": ["Most reliable", "Multiple backup options"],
        "cons": ["More complex setup"]
    }
}

def show_resume_options():
    """Display available resume handling options"""
    print("📄 Resume Handling Options")
    print("=" * 40)
    
    for option_id, option in RESUME_HANDLING_OPTIONS.items():
        print(f"\n{option['name']}")
        print(f"Description: {option['description']}")
        print("Pros:", ", ".join(option['pros']))
        print("Cons:", ", ".join(option['cons']))
    
    print("\n🎯 Recommended Approach:")
    print("Start with Option 1 (Local Storage + Google Forms URL)")
    print("Upgrade to Option 4 (Hybrid) for production")

if __name__ == "__main__":
    show_resume_options()

