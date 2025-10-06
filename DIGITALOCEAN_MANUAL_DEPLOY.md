# 🚀 DigitalOcean Manual Deployment Guide

Since DigitalOcean needs GitHub authentication, let's deploy through the web interface:

## 📋 **Step-by-Step Deployment**

### **1. Go to DigitalOcean App Platform**
- Visit: [cloud.digitalocean.com/apps](https://cloud.digitalocean.com/apps)
- Click **"Create App"**

### **2. Connect GitHub Repository**
- Select **"GitHub"** as source
- **Authorize DigitalOcean** to access your GitHub account
- Select repository: **`yaro360/EducationEdJoin`**
- Select branch: **`main`**

### **3. Configure Your App**

#### **Web Service:**
- **Name**: `web`
- **Source Directory**: `/` (root)
- **Build Command**: `pip install -r requirements.txt`
- **Run Command**: `gunicorn app:app`
- **HTTP Port**: `8080`
- **Instance Size**: `Basic XXS` ($5/month)

#### **Environment Variables:**
```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this-in-production
```

### **4. Add Scheduled Job (Scraper)**
- Click **"Add Component"** → **"Job"**
- **Name**: `scraper`
- **Source Directory**: `/`
- **Run Command**: `python3 production_scraper.py`
- **Instance Size**: `Basic XXS`
- **Schedule**: `0 6 * * *` (runs daily at 6 AM)

### **5. Deploy**
- Click **"Create Resources"**
- Wait 5-10 minutes for deployment
- Your app will be available at: `https://education-jobs-dashboard-xxxxx.ondigitalocean.app`

## 🔧 **After Deployment**

### **Set Up Google Forms Integration:**
1. Go to your app in DigitalOcean dashboard
2. Click **"Settings"** → **"App-Level Environment Variables"**
3. Add these variables:
   ```
   GOOGLE_FORMS_URL=your-google-form-submission-url
   GOOGLE_FORMS_ENTRY_NAME=entry.1234567890
   GOOGLE_FORMS_ENTRY_EMAIL=entry.9876543210
   GOOGLE_FORMS_ENTRY_PHONE=entry.1122334455
   GOOGLE_FORMS_ENTRY_EXPERIENCE=entry.2233445566
   GOOGLE_FORMS_ENTRY_EDUCATION=entry.3344556677
   GOOGLE_FORMS_ENTRY_ROLES=entry.4455667788
   GOOGLE_FORMS_ENTRY_LOCATIONS=entry.5566778899
   GOOGLE_FORMS_ENTRY_SKILLS=entry.6677889900
   GOOGLE_FORMS_ENTRY_RESUME_URL=entry.7788990011
   GOOGLE_FORMS_ENTRY_TIMESTAMP=entry.8899001122
   ```

### **Test Your App:**
- Visit your app URL
- Test the job dashboard
- Test candidate registration
- Test the embeddable widget

## 📱 **Squarespace Integration**

Once deployed, embed your dashboard using:
```html
<iframe src="https://your-app-url.ondigitalocean.app/embed-enhanced" 
        width="100%" 
        height="600" 
        frameborder="0">
</iframe>
```

## 💰 **Cost Breakdown**
- **Web Service**: $5/month
- **Scheduled Job**: $5/month (only runs when scheduled)
- **Total**: ~$5-10/month

## 🆘 **Troubleshooting**

### **Common Issues:**
1. **Build fails**: Check `requirements.txt` has all dependencies
2. **App won't start**: Check environment variables
3. **Scraper not running**: Check job schedule and logs
4. **GitHub auth issues**: Re-authorize in DigitalOcean settings

### **Check Logs:**
- Go to your app dashboard
- Click **"Runtime Logs"** to see what's happening
- Click **"Build Logs"** to see build process

---

**Ready to deploy?** Follow the steps above in the DigitalOcean web interface! 🚀
