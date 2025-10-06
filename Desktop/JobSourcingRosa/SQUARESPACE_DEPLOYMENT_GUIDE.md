# 🚀 Squarespace Deployment Guide

## 📋 Overview

This guide will help you deploy your Education Jobs Sourcing Tool and embed it into your Squarespace website. We'll cover hosting, file storage, and step-by-step implementation.

---

## 🏗️ **Step 1: Choose Your Hosting Platform**

### **Option A: Heroku (Recommended - Easiest)**
- ✅ **Free tier available** (with limitations)
- ✅ **Easy deployment** with Git
- ✅ **Automatic scaling**
- ✅ **Built-in database**

### **Option B: DigitalOcean (Recommended - Most Reliable)**
- ✅ **$5/month droplet**
- ✅ **Full control**
- ✅ **Better for file storage**
- ✅ **More reliable**

### **Option C: Railway/Render (Alternative)**
- ✅ **Modern platform**
- ✅ **Easy deployment**
- ✅ **Good free tier**

---

## 🚀 **Step 2: Deploy to Heroku (Recommended)**

### **2.1: Prepare Your Code**

```bash
# 1. Create a new Git repository
cd /Users/yco/Desktop/JobSourcingRosa
git init
git add .
git commit -m "Initial commit - Education Jobs Sourcing Tool"

# 2. Create .gitignore
echo "uploads/" >> .gitignore
echo "*.log" >> .gitignore
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
```

### **2.2: Create Heroku App**

```bash
# 1. Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login to Heroku
heroku login

# 3. Create app
heroku create your-education-jobs-app

# 4. Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-super-secret-key-here

# 5. Deploy
git push heroku main
```

### **2.3: Set Up File Storage**

Since Heroku has ephemeral file system, we need cloud storage:

```bash
# Install AWS S3 for file storage
pip install boto3

# Add to requirements.txt
echo "boto3==1.34.0" >> requirements.txt
```

---

## 🏗️ **Step 3: Deploy to DigitalOcean (More Reliable)**

### **3.1: Create Droplet**

1. **Go to DigitalOcean**
2. **Create Droplet**
3. **Choose Ubuntu 22.04**
4. **Select $5/month plan**
5. **Add SSH key**
6. **Create droplet**

### **3.2: Set Up Server**

```bash
# SSH into your droplet
ssh root@your-droplet-ip

# Update system
apt update && apt upgrade -y

# Install Python and dependencies
apt install python3 python3-pip python3-venv nginx git -y

# Create app directory
mkdir -p /var/www/education-jobs
cd /var/www/education-jobs

# Clone your repository
git clone https://github.com/your-username/JobSourcingRosa.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create uploads directory
mkdir uploads
chmod 755 uploads

# Set up Gunicorn
pip install gunicorn
```

### **3.3: Configure Nginx**

```bash
# Create Nginx configuration
nano /etc/nginx/sites-available/education-jobs

# Add this content:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /uploads/ {
        alias /var/www/education-jobs/uploads/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}

# Enable site
ln -s /etc/nginx/sites-available/education-jobs /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### **3.4: Set Up Systemd Service**

```bash
# Create service file
nano /etc/systemd/system/education-jobs.service

# Add this content:
[Unit]
Description=Education Jobs Sourcing Tool
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/education-jobs
Environment=PATH=/var/www/education-jobs/venv/bin
ExecStart=/var/www/education-jobs/venv/bin/gunicorn --bind 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
systemctl enable education-jobs
systemctl start education-jobs
systemctl status education-jobs
```

---

## 📁 **Step 4: File Storage Solutions**

### **Option A: Local Storage (DigitalOcean)**
```python
# Files stored in: /var/www/education-jobs/uploads/
# Accessible via: https://your-domain.com/uploads/filename.pdf
```

### **Option B: AWS S3 (Recommended for Heroku)**
```python
# 1. Create S3 bucket
# 2. Set up IAM user with S3 permissions
# 3. Configure environment variables

# Add to your app.py:
import boto3
from botocore.exceptions import ClientError

def upload_to_s3(file, bucket_name, object_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_fileobj(file, bucket_name, object_name)
        return f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return None
```

### **Option C: Google Drive (Alternative)**
```python
# Use Google Drive API for file storage
# Already implemented in your resume_handling.py
```

---

## 🔗 **Step 5: Embed in Squarespace**

### **5.1: Get Your App URL**

After deployment, you'll have:
- **Main Dashboard**: `https://your-app.herokuapp.com/`
- **Embed Widget**: `https://your-app.herokuapp.com/embed-enhanced`
- **Admin Panel**: `https://your-app.herokuapp.com/admin/applications`

### **5.2: Add to Squarespace**

#### **Method 1: Code Block (Easiest)**

1. **Go to your Squarespace site**
2. **Edit the page where you want the job board**
3. **Add a Code Block**
4. **Paste this code:**

```html
<div id="education-jobs-widget">
    <iframe 
        src="https://your-app.herokuapp.com/embed-enhanced" 
        width="100%" 
        height="800" 
        frameborder="0"
        style="border: none; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    </iframe>
</div>

<style>
#education-jobs-widget {
    margin: 20px 0;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 12px;
}

#education-jobs-widget iframe {
    min-height: 600px;
}

@media (max-width: 768px) {
    #education-jobs-widget iframe {
        height: 1000px;
    }
}
</style>
```

#### **Method 2: Custom CSS + JavaScript**

1. **Add to Page Settings > Advanced > Page Header Code Injection:**

```html
<link rel="stylesheet" href="https://your-app.herokuapp.com/static/css/widget.css">
<script src="https://your-app.herokuapp.com/static/js/widget.js"></script>
```

2. **Add to Page Content:**

```html
<div class="education-jobs-container">
    <div id="jobs-widget"></div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    loadJobsWidget('https://your-app.herokuapp.com/embed-enhanced');
});
</script>
```

---

## 🎨 **Step 6: Customize for Squarespace**

### **6.1: Match Your Brand Colors**

```css
/* Add to your Squarespace Custom CSS */
.education-jobs-widget {
    --primary-color: #your-brand-color;
    --secondary-color: #your-secondary-color;
    --text-color: #your-text-color;
    --background-color: #your-background-color;
}

.education-jobs-widget .job-card {
    border-left: 4px solid var(--primary-color);
}

.education-jobs-widget .btn-primary {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
}
```

### **6.2: Responsive Design**

```css
/* Mobile optimization */
@media (max-width: 768px) {
    .education-jobs-widget iframe {
        height: 1200px !important;
    }
    
    .education-jobs-widget .job-card {
        margin-bottom: 15px;
    }
}
```

---

## 🔧 **Step 7: Set Up Auto-Refresh**

### **7.1: Heroku Scheduler**

```bash
# Install Heroku Scheduler addon
heroku addons:create scheduler:standard

# Add job to scheduler
# Command: python3 production_scraper.py
# Frequency: Daily at 6 AM
```

### **7.2: DigitalOcean Cron**

```bash
# Add to crontab
crontab -e

# Add this line:
0 6 * * * cd /var/www/education-jobs && /var/www/education-jobs/venv/bin/python production_scraper.py >> /var/log/job_refresh.log 2>&1
```

---

## 📊 **Step 8: Monitor and Maintain**

### **8.1: Health Checks**

```python
# Add to your app.py
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'positions': len(load_jobs())
    })
```

### **8.2: Log Monitoring**

```bash
# Heroku logs
heroku logs --tail

# DigitalOcean logs
journalctl -u education-jobs -f
```

---

## 🎯 **Step 9: Complete Implementation Checklist**

### **✅ Deployment Checklist:**
- [ ] Code deployed to hosting platform
- [ ] Environment variables configured
- [ ] File storage set up (S3 or local)
- [ ] Domain configured (optional)
- [ ] SSL certificate installed
- [ ] Auto-refresh scheduled

### **✅ Squarespace Integration Checklist:**
- [ ] Widget embedded in Squarespace
- [ ] Responsive design tested
- [ ] Brand colors customized
- [ ] Mobile view optimized
- [ ] Admin panel accessible

### **✅ Testing Checklist:**
- [ ] Job listings display correctly
- [ ] Candidate registration works
- [ ] Resume uploads function
- [ ] Admin panel accessible
- [ ] Auto-refresh working
- [ ] Mobile responsive

---

## 🚀 **Quick Start Commands**

### **For Heroku:**
```bash
# 1. Deploy
git push heroku main

# 2. Set up scheduler
heroku addons:create scheduler:standard

# 3. Check logs
heroku logs --tail
```

### **For DigitalOcean:**
```bash
# 1. Deploy
git pull origin main
systemctl restart education-jobs

# 2. Set up cron
crontab -e
# Add: 0 6 * * * cd /var/www/education-jobs && python3 production_scraper.py

# 3. Check status
systemctl status education-jobs
```

---

## 🎉 **Final Result**

After implementation, you'll have:

✅ **Professional job board** embedded in Squarespace  
✅ **Automatic job updates** every 24 hours  
✅ **Resume upload system** with cloud storage  
✅ **Admin panel** for managing applications  
✅ **Mobile responsive** design  
✅ **Branded appearance** matching your site  

**Your Education Jobs Sourcing Tool will be live and fully functional on your Squarespace site!** 🚀

---

## 📞 **Need Help?**

If you encounter any issues:
1. Check the logs: `heroku logs --tail` or `journalctl -u education-jobs -f`
2. Verify environment variables are set
3. Test the health endpoint: `https://your-app.herokuapp.com/health`
4. Check file permissions for uploads directory

**Ready to deploy? Let's get your job board live!** 🚀
