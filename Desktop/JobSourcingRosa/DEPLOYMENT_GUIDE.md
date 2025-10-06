# 🚀 Deployment Guide - External Access & Squarespace Integration

## 📋 Quick Setup Checklist

### 1. Google Forms Setup
- [ ] Create Google Form with candidate fields
- [ ] Get form submission URL and entry IDs
- [ ] Configure Google Forms integration

### 2. External Access Setup
- [ ] Deploy to cloud platform (Heroku/DigitalOcean)
- [ ] Configure domain and SSL
- [ ] Test external access

### 3. Squarespace Integration
- [ ] Add embed code to Squarespace
- [ ] Test functionality
- [ ] Configure styling

---

## 🔧 Step 1: Google Forms Integration

### Create Your Google Form

1. **Go to Google Forms**: https://forms.google.com
2. **Create New Form**: "Education Leadership Candidate Registration"
3. **Add Fields** (exactly as shown below):

```
📝 Form Fields:
- Full Name (Short Answer) - Required
- Email Address (Short Answer) - Required  
- Phone Number (Short Answer) - Optional
- Years of Experience (Multiple Choice) - Required
- Education Level (Multiple Choice) - Required
- Preferred Roles (Checkboxes) - Required
- Preferred Locations (Short Answer) - Optional
- Key Skills (Short Answer) - Optional
- Resume URL (Short Answer) - Optional
- Registration Timestamp (Short Answer) - Optional
```

### Get Form Entry IDs

1. **Open your form in edit mode**
2. **Right-click on each field** → "Inspect Element"
3. **Find the 'name' attribute** (e.g., `entry.1234567890`)
4. **Copy all entry IDs**

### Configure Integration

Update `google_forms_integration.py`:

```python
# Replace with your actual Google Form URL
self.forms_url = 'https://docs.google.com/forms/d/YOUR_FORM_ID/formResponse'

# Replace with your actual entry IDs
self.field_mapping = {
    'entry.1234567890': 'name',           # Your actual entry ID
    'entry.1234567891': 'email',         # Your actual entry ID
    'entry.1234567892': 'phone',         # Your actual entry ID
    # ... etc
}
```

---

## 🌐 Step 2: External Access Setup

### Option A: Heroku (Free & Easy)

```bash
# 1. Install Heroku CLI
# 2. Login to Heroku
heroku login

# 3. Create app
heroku create your-education-jobs-app

# 4. Set environment variables
heroku config:set GOOGLE_FORMS_URL="https://docs.google.com/forms/d/YOUR_FORM_ID/formResponse"
heroku config:set FLASK_SECRET_KEY="your-secret-key"

# 5. Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main

# 6. Your app will be available at:
# https://your-education-jobs-app.herokuapp.com
```

### Option B: DigitalOcean App Platform

1. **Connect GitHub repository**
2. **Set environment variables**:
   - `GOOGLE_FORMS_URL`
   - `FLASK_SECRET_KEY`
3. **Deploy automatically**
4. **Get your custom domain**

### Option C: VPS/Server

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Set environment variables
export GOOGLE_FORMS_URL="https://docs.google.com/forms/d/YOUR_FORM_ID/formResponse"
export FLASK_SECRET_KEY="your-secret-key"

# 3. Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 4. Set up Nginx reverse proxy
# 5. Configure SSL certificate
```

---

## 🎨 Step 3: Squarespace Integration

### Method 1: Embed Widget (Recommended)

1. **Go to your Squarespace site**
2. **Add a "Code Block"**
3. **Paste this code**:

```html
<div style="width: 100%; max-width: 1200px; margin: 0 auto;">
    <iframe 
        src="https://your-domain.com/embed-enhanced" 
        width="100%" 
        height="900px" 
        frameborder="0"
        style="border: none; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
    </iframe>
</div>
```

### Method 2: Custom Page Integration

1. **Create a new page** in Squarespace
2. **Add Code Block** with the embed code above
3. **Customize styling** to match your brand

### Method 3: Full Page Replacement

1. **Create a new page**
2. **Use only the embed code** (no other content)
3. **Make it full-width**

---

## 🎯 Squarespace-Specific Code

### Responsive Embed Code

```html
<style>
    .education-jobs-widget {
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .education-jobs-widget iframe {
        width: 100%;
        height: 900px;
        border: none;
    }
    
    @media (max-width: 768px) {
        .education-jobs-widget iframe {
            height: 700px;
        }
    }
    
    @media (max-width: 480px) {
        .education-jobs-widget iframe {
            height: 600px;
        }
    }
</style>

<div class="education-jobs-widget">
    <iframe src="https://your-domain.com/embed-enhanced"></iframe>
</div>
```

### Branded Integration

```html
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px;
    border-radius: 12px;
    margin: 20px 0;
">
    <h2 style="color: white; text-align: center; margin-bottom: 20px;">
        🎓 Education Leadership Positions
    </h2>
    <p style="color: white; text-align: center; margin-bottom: 20px;">
        Discover director, dean, and assistant director positions from EdJoin.org
    </p>
    <iframe 
        src="https://your-domain.com/embed-enhanced" 
        width="100%" 
        height="800px" 
        frameborder="0"
        style="border-radius: 8px; background: white;">
    </iframe>
</div>
```

---

## 🔧 Configuration Files

### Environment Variables (.env)

```env
# Google Forms Integration
GOOGLE_FORMS_URL=https://docs.google.com/forms/d/YOUR_FORM_ID/formResponse

# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-change-this
FLASK_DEBUG=False

# Domain Configuration
DOMAIN=https://your-domain.com

# Google Sheets (Optional)
GOOGLE_SHEET_NAME=EdJoin Education Jobs
SERVICE_ACCOUNT_FILE=service_account.json
```

### Procfile (for Heroku)

```
web: gunicorn app:app
```

### requirements.txt (Updated)

```
requests==2.31.0
beautifulsoup4==4.12.2
gspread==5.12.4
google-auth==2.23.4
flask==3.0.0
selenium==4.15.2
webdriver-manager==4.0.1
schedule==1.2.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

---

## 🧪 Testing Checklist

### Before Going Live

- [ ] **Google Forms**: Test form submission
- [ ] **External Access**: Test from different devices/locations
- [ ] **Squarespace**: Test embed on your site
- [ ] **Mobile**: Test on mobile devices
- [ ] **SSL**: Ensure HTTPS is working
- [ ] **Performance**: Test loading speed

### Test URLs

- **Main Dashboard**: `https://your-domain.com/`
- **Enhanced Widget**: `https://your-domain.com/embed-enhanced`
- **Candidate Registration**: `https://your-domain.com/candidate/register`
- **Admin Panel**: `https://your-domain.com/admin/applications`

---

## 🚀 Quick Deploy Commands

### Heroku Deployment

```bash
# One-time setup
heroku create your-app-name
heroku config:set GOOGLE_FORMS_URL="https://docs.google.com/forms/d/YOUR_FORM_ID/formResponse"

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main

# Open your app
heroku open
```

### Test Locally First

```bash
# Set environment variables
export GOOGLE_FORMS_URL="https://docs.google.com/forms/d/YOUR_FORM_ID/formResponse"
export FLASK_SECRET_KEY="test-secret-key"

# Run locally
python3 app.py

# Test at http://localhost:5000
```

---

## 📞 Support & Troubleshooting

### Common Issues

1. **Google Forms not receiving data**
   - Check entry IDs are correct
   - Verify form URL is correct
   - Test form submission manually

2. **Squarespace embed not working**
   - Check iframe URL is accessible
   - Verify HTTPS is enabled
   - Test on different browsers

3. **External access issues**
   - Check firewall settings
   - Verify domain configuration
   - Test SSL certificate

### Getting Help

1. Check the browser console for errors
2. Test each component separately
3. Verify all environment variables are set
4. Check server logs for detailed error messages

---

## 🎉 Final Result

Once deployed, you'll have:

✅ **External Access**: Your client can access from anywhere  
✅ **Google Forms Integration**: All candidate data goes to your Google Form  
✅ **Squarespace Integration**: Beautiful widget on your website  
✅ **Mobile Responsive**: Works on all devices  
✅ **Professional Branding**: Matches your website design  
✅ **Real-time Data**: Live job postings from EdJoin.org  
✅ **AI Matching**: Smart candidate-job pairing  

**Your Education Jobs Sourcing Tool will be live and ready for your client!** 🚀
