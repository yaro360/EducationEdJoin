# 📄 Resume Handling Guide

## 🎯 The Challenge with Google Forms

**Google Forms Limitation**: Google Forms can only handle file uploads in specific scenarios and has size limits. For professional resume handling, we need alternative approaches.

## 🚀 Best Solutions for Resume Handling

### **Option 1: Local Storage + Google Forms URL (Recommended for Start)**

**How it works:**
1. Candidate uploads resume to your server
2. Resume is saved locally with a unique filename
3. Download URL is included in Google Form submission
4. You can access resumes via the provided URL

**Pros:**
- ✅ Simple to implement
- ✅ Works immediately
- ✅ No additional setup required
- ✅ Reliable and fast

**Cons:**
- ⚠️ Requires server storage space
- ⚠️ URLs may change if server restarts

**Setup:**
```python
# Already implemented in your app!
# Resumes are saved to /uploads/ folder
# URLs are automatically included in Google Form submissions
```

---

### **Option 2: Google Drive Integration (Professional)**

**How it works:**
1. Candidate uploads resume to your server
2. Resume is automatically uploaded to Google Drive
3. Public shareable link is generated
4. Link is included in Google Form submission

**Pros:**
- ✅ Professional and reliable
- ✅ Easy access from anywhere
- ✅ Automatic backup
- ✅ No server storage needed

**Cons:**
- ⚠️ Requires Google Drive API setup
- ⚠️ More complex configuration

**Setup:**
```bash
# 1. Enable Google Drive API
# 2. Create service account credentials
# 3. Create shared folder in Google Drive
# 4. Set environment variables:
export GOOGLE_DRIVE_FOLDER_ID="your_folder_id"
```

---

### **Option 3: Email with Attachments (Direct Delivery)**

**How it works:**
1. Candidate uploads resume
2. Resume is attached to email
3. Email is sent to admin with candidate details
4. Google Form also receives candidate data

**Pros:**
- ✅ Direct delivery to admin
- ✅ Immediate notification
- ✅ No storage management needed
- ✅ Works with any email provider

**Cons:**
- ⚠️ Email size limits (usually 25MB)
- ⚠️ Requires email server setup

**Setup:**
```bash
# Set email configuration:
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export EMAIL_USER="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export ADMIN_EMAIL="admin@yourcompany.com"
```

---

### **Option 4: Hybrid Approach (Most Reliable)**

**How it works:**
1. Resume is saved locally (backup)
2. Resume is uploaded to Google Drive (primary)
3. Email notification is sent to admin
4. Google Form receives all data + resume URL

**Pros:**
- ✅ Maximum reliability
- ✅ Multiple access methods
- ✅ Professional setup
- ✅ Backup options

**Cons:**
- ⚠️ Most complex setup
- ⚠️ Multiple services to configure

---

## 🛠️ Implementation Guide

### **Current Implementation (Option 1)**

Your app currently uses **Option 1** - Local Storage + Google Forms URL:

```python
# Resumes are automatically:
# 1. Saved to /uploads/ folder
# 2. Given unique filenames
# 3. URLs included in Google Form submissions
# 4. Accessible via /uploads/filename endpoint
```

### **Upgrading to Option 2 (Google Drive)**

1. **Enable Google Drive API:**
   - Go to Google Cloud Console
   - Enable Google Drive API
   - Create service account credentials

2. **Create Google Drive Folder:**
   - Create a folder in Google Drive
   - Share with service account email
   - Copy folder ID

3. **Update Configuration:**
   ```bash
   export GOOGLE_DRIVE_FOLDER_ID="your_folder_id_here"
   ```

4. **Update Google Form:**
   - Add "Resume URL" field to your Google Form
   - The app will automatically populate this field

### **Adding Option 3 (Email)**

1. **Set up Email Configuration:**
   ```bash
   export SMTP_SERVER="smtp.gmail.com"
   export SMTP_PORT="587"
   export EMAIL_USER="your-email@gmail.com"
   export EMAIL_PASSWORD="your-app-password"
   export ADMIN_EMAIL="admin@yourcompany.com"
   ```

2. **Enable Gmail App Passwords:**
   - Go to Google Account settings
   - Enable 2-factor authentication
   - Generate app password for this application

---

## 📋 Google Form Setup for Resumes

### **Required Fields in Google Form:**

```
📝 Google Form Fields:
- Full Name (Short Answer) - Required
- Email Address (Short Answer) - Required
- Phone Number (Short Answer) - Optional
- Years of Experience (Multiple Choice) - Required
- Education Level (Multiple Choice) - Required
- Preferred Roles (Checkboxes) - Required
- Preferred Locations (Short Answer) - Optional
- Key Skills (Short Answer) - Optional
- Resume URL (Short Answer) - Optional ⭐ NEW FIELD
- Registration Timestamp (Short Answer) - Optional
```

### **Getting Entry IDs:**

1. **Open your Google Form in edit mode**
2. **Right-click on "Resume URL" field**
3. **Select "Inspect Element"**
4. **Find the 'name' attribute** (e.g., `entry.1234567890`)
5. **Update `google_forms_integration.py`:**

```python
self.field_mapping = {
    'entry.1234567890': 'name',
    'entry.1234567891': 'email',
    'entry.1234567892': 'phone',
    'entry.1234567893': 'years_experience',
    'entry.1234567894': 'education_level',
    'entry.1234567895': 'preferred_roles',
    'entry.1234567896': 'preferred_locations',
    'entry.1234567897': 'skills',
    'entry.1234567898': 'resume_url',  # ⭐ Resume URL field
    'entry.1234567899': 'timestamp'
}
```

---

## 🧪 Testing Resume Upload

### **Test Locally:**

1. **Start your app:**
   ```bash
   python3 app.py
   ```

2. **Go to candidate registration:**
   ```
   http://localhost:5000/candidate/register
   ```

3. **Fill out form and upload resume**

4. **Check results:**
   - Check `/uploads/` folder for saved file
   - Check Google Form for new submission
   - Check email (if configured)

### **Test Resume Access:**

1. **Upload a resume**
2. **Note the filename from the success message**
3. **Access resume directly:**
   ```
   http://localhost:5000/uploads/filename.pdf
   ```

---

## 🚀 Deployment Considerations

### **For Heroku:**
- ✅ Local storage works (ephemeral)
- ✅ Google Drive recommended for persistence
- ✅ Email notifications work well

### **For DigitalOcean/VPS:**
- ✅ Local storage works (persistent)
- ✅ All options available
- ✅ Can use hybrid approach

### **For Squarespace Integration:**
- ✅ Resume uploads work in embedded widget
- ✅ URLs are accessible externally
- ✅ Professional user experience

---

## 📊 Resume Handling Flow

```
1. Candidate visits your website
   ↓
2. Fills out registration form
   ↓
3. Uploads resume (PDF/DOC/DOCX)
   ↓
4. Resume saved to server with unique filename
   ↓
5. Resume URL added to candidate data
   ↓
6. All data submitted to Google Form
   ↓
7. Optional: Resume uploaded to Google Drive
   ↓
8. Optional: Email sent to admin with resume
   ↓
9. Candidate sees success message with job matches
```

---

## 🎯 Recommended Setup for Your Client

### **Phase 1: Basic Setup (Start Here)**
- ✅ Use Option 1 (Local Storage + Google Forms URL)
- ✅ Set up Google Form with Resume URL field
- ✅ Deploy to Heroku/DigitalOcean
- ✅ Test with client

### **Phase 2: Professional Setup (Upgrade Later)**
- ✅ Add Google Drive integration
- ✅ Add email notifications
- ✅ Implement hybrid approach
- ✅ Add resume management features

---

## 🔧 Troubleshooting

### **Common Issues:**

1. **Resume not uploading:**
   - Check file size (max 10MB)
   - Check file format (PDF, DOC, DOCX only)
   - Check server permissions

2. **Google Form not receiving resume URL:**
   - Verify entry ID is correct
   - Check form URL is correct
   - Test form submission manually

3. **Resume URL not accessible:**
   - Check server is running
   - Verify file was saved correctly
   - Check URL format

### **Debug Steps:**

1. **Check uploads folder:**
   ```bash
   ls -la uploads/
   ```

2. **Test resume URL directly:**
   ```
   http://your-domain.com/uploads/filename.pdf
   ```

3. **Check Google Form submissions:**
   - Go to Google Forms
   - Click "Responses" tab
   - Check for new submissions

---

## 🎉 Final Result

With resume handling implemented, you'll have:

✅ **Professional Resume Upload** - Candidates can upload PDFs, DOCs, DOCX  
✅ **Google Forms Integration** - Resume URLs automatically included  
✅ **Multiple Access Methods** - Local storage, Google Drive, email  
✅ **Reliable Backup Options** - Multiple ways to access resumes  
✅ **Professional User Experience** - Seamless upload process  
✅ **Admin Notifications** - Email alerts for new candidates  

**Your Education Jobs Sourcing Tool now handles resumes professionally!** 🚀

