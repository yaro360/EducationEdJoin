# 🌐 Website Integration Guide

## Your Complete Education Jobs Sourcing Solution

### 🎯 What You Now Have

✅ **Complete Job Sourcing Tool** that scrapes director-level positions from EdJoin.org  
✅ **AI-Powered Candidate Matching** system that pairs candidates with suitable positions  
✅ **Professional Web Dashboard** with filtering and application system  
✅ **Embeddable Widgets** for any website  
✅ **Resume Upload System** for candidates  
✅ **Google Sheets Integration** for data management  
✅ **Admin Panels** for managing applications and candidates  

---

## 🚀 How to Embed on Your Website

### Option 1: Simple Job Listings Widget

Add this code to any page on your website:

```html
<iframe 
    src="http://your-domain.com/embed" 
    width="100%" 
    height="800px" 
    frameborder="0"
    style="border: none; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
</iframe>
```

**What visitors see:**
- Live job listings from EdJoin.org
- Filter by role (Director, Assistant Director, Dean, Principal)
- Direct links to apply on EdJoin.org
- Professional, responsive design

### Option 2: Enhanced Widget with Candidate Registration

```html
<iframe 
    src="http://your-domain.com/embed-enhanced" 
    width="100%" 
    height="900px" 
    frameborder="0"
    style="border: none; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
</iframe>
```

**What visitors see:**
- All features from Option 1 PLUS:
- "Join Talent Pool" call-to-action
- Candidate registration form
- AI-powered job matching
- Personalized job recommendations

---

## 🎯 Candidate Matching System

### How It Works

1. **Candidates Register** through your website widget
2. **AI Analyzes** their profile (experience, education, preferences)
3. **System Matches** them with suitable positions
4. **Candidates Get** personalized job recommendations
5. **You Get** qualified candidates in your database

### Matching Criteria

- **Role Preference** (40 points) - How well the position matches their preferred roles
- **Location** (25 points) - Geographic alignment with preferred locations  
- **Experience Level** (20 points) - Whether their experience matches requirements
- **Education** (10 points) - Educational background compatibility
- **Skills** (5 points) - Keyword matching between skills and job requirements

### Candidate Dashboard

Each candidate gets a personalized dashboard showing:
- Their profile information
- Recommended positions with match scores
- Direct application links
- Why each position is a good match

---

## 📱 Platform-Specific Instructions

### WordPress
1. Edit your page/post
2. Switch to "Text" or "HTML" mode
3. Paste the iframe code
4. Update/Publish

### Squarespace
1. Add a "Code Block"
2. Paste the iframe code
3. Save

### Wix
1. Add "Embed" element
2. Choose "Custom Code"
3. Paste the iframe code

### Shopify
1. Go to Online Store > Themes
2. Edit your theme
3. Add iframe code to desired template

### Custom Website
Simply add the iframe code to your HTML where you want the widget to appear.

---

## 🔧 Customization Options

### Custom Styling
```html
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 12px;
    margin: 20px 0;
">
    <h2 style="color: white; text-align: center; margin-bottom: 20px;">
        🎓 Education Leadership Positions
    </h2>
    <iframe 
        src="http://your-domain.com/embed-enhanced" 
        width="100%" 
        height="700px" 
        frameborder="0"
        style="border-radius: 8px; background: white;">
    </iframe>
</div>
```

### Mobile Responsive
```html
<style>
    .jobs-widget {
        width: 100%;
        height: 600px;
    }
    
    @media (max-width: 768px) {
        .jobs-widget {
            height: 500px;
        }
    }
</style>

<div class="jobs-widget">
    <iframe 
        src="http://your-domain.com/embed-enhanced" 
        width="100%" 
        height="100%" 
        frameborder="0">
    </iframe>
</div>
```

---

## 🚀 Deployment Options

### 1. Heroku (Free & Easy)
```bash
# One-time setup
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
git push heroku main

# Your widget URL becomes:
# https://your-app-name.herokuapp.com/embed-enhanced
```

### 2. DigitalOcean App Platform
1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically
4. Get your custom domain

### 3. VPS/Server
```bash
# Install and run
pip3 install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Set up Nginx reverse proxy
# Configure SSL certificate
```

---

## 📊 Admin Features

### View All Candidates
- Access: `http://your-domain.com/admin/candidates`
- See all registered candidates
- View their match scores
- Download resumes

### View Applications
- Access: `http://your-domain.com/admin/applications`
- See job applications
- Download candidate resumes
- Contact candidates directly

### Google Sheets Integration
- Automatic data sync
- Real-time job updates
- Easy data export

---

## 🎯 Business Benefits

### For You
- **Automated Job Sourcing** - No manual work needed
- **Qualified Candidates** - AI matching brings the right people
- **Professional Branding** - Beautiful, responsive widgets
- **Data Management** - Google Sheets integration
- **Scalable Solution** - Works for any number of positions

### For Candidates
- **Personalized Experience** - Get matched with relevant positions
- **Easy Application** - One-click application process
- **Professional Platform** - Clean, modern interface
- **Direct Access** - Apply directly through your website

### For Employers
- **Quality Candidates** - Pre-screened and matched
- **Time Savings** - No need to post on multiple job boards
- **Brand Visibility** - Your website becomes a job destination
- **Data Insights** - Track candidate engagement

---

## 🔗 API Integration

### Get Jobs Data
```javascript
fetch('http://your-domain.com/api/jobs')
    .then(response => response.json())
    .then(jobs => {
        // Display jobs in your custom layout
        displayJobs(jobs);
    });
```

### Get Candidate Matches
```javascript
fetch('http://your-domain.com/api/candidate-matches/candidate_id')
    .then(response => response.json())
    .then(matches => {
        // Display personalized matches
        displayMatches(matches);
    });
```

---

## 🎉 Ready to Launch!

### Quick Start Checklist
- [ ] Deploy your application (Heroku, DigitalOcean, etc.)
- [ ] Get your domain URL
- [ ] Add iframe code to your website
- [ ] Test on mobile devices
- [ ] Set up Google Sheets (optional)
- [ ] Configure email notifications (optional)

### Your Widget URLs
- **Simple Widget**: `https://your-domain.com/embed`
- **Enhanced Widget**: `https://your-domain.com/embed-enhanced`
- **Main Dashboard**: `https://your-domain.com/`
- **Candidate Registration**: `https://your-domain.com/candidate/register`

---

## 📞 Support & Customization

The system is fully customizable:
- **Colors & Branding** - Edit CSS in templates
- **Matching Algorithm** - Adjust scoring in `candidate_matching.py`
- **Job Sources** - Add more job boards in `edjoin_scraper.py`
- **Email Templates** - Customize notification emails
- **Admin Features** - Add more management tools

**Your Education Jobs Sourcing Tool is ready to help you find the perfect candidates for education leadership positions!** 🚀

---

*Need help with deployment or customization? The code is well-documented and includes comprehensive error handling and logging.*

