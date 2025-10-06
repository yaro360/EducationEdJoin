# 🐙 GitHub Setup Guide

## 🎯 **Step 1: Create New GitHub Repository**

### **Option A: Using GitHub Website (Recommended)**
1. **Go to**: https://github.com/new
2. **Repository name**: `education-jobs-sourcing-tool`
3. **Description**: `Professional job board for education positions with EdJoin.org scraping, candidate management, and Squarespace integration`
4. **Visibility**: Public (or Private if you prefer)
5. **Initialize**: Don't check "Add a README file" (we already have one)
6. **Click**: "Create repository"

### **Option B: Using GitHub CLI (if installed)**
```bash
gh repo create education-jobs-sourcing-tool --public --description "Professional job board for education positions with EdJoin.org scraping, candidate management, and Squarespace integration"
```

---

## 🔗 **Step 2: Update Remote Repository**

After creating the repository, run these commands:

```bash
# Remove old remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/yaro360/education-jobs-sourcing-tool.git

# Push to new repository
git push -u origin main
```

---

## 📋 **Step 3: Verify Upload**

Check that everything uploaded correctly:
- Go to: https://github.com/yaro360/education-jobs-sourcing-tool
- Verify all files are there
- Check that the README displays properly

---

## 🚀 **Step 4: Ready for Deployment**

Once on GitHub, you can deploy using either:

### **Heroku (from GitHub):**
```bash
# Heroku can connect directly to GitHub
heroku create education-jobs-rosa
heroku git:remote -a education-jobs-rosa
git push heroku main
```

### **DigitalOcean (from GitHub):**
```bash
# Clone on your droplet
git clone https://github.com/yaro360/education-jobs-sourcing-tool.git
cd education-jobs-sourcing-tool
sudo ./deploy_to_digitalocean.sh
```

---

## 📊 **What's Included in Your Repository**

✅ **Complete Flask Application** (app.py)  
✅ **Multi-page Scraper** (production_scraper.py)  
✅ **Auto-refresh System** (auto_refresh_system.py)  
✅ **Deployment Scripts** (deploy_to_heroku.py, deploy_to_digitalocean.sh)  
✅ **Templates** (HTML files for UI)  
✅ **Documentation** (Multiple guides)  
✅ **Configuration** (requirements.txt, Procfile)  
✅ **29 Job Positions** (edjoin_jobs.json)  

---

## 🎯 **Next Steps After GitHub Upload**

1. **Create the GitHub repository** (follow Step 1)
2. **Update remote and push** (follow Step 2)
3. **Choose deployment method**:
   - **Heroku**: `python3 deploy_to_heroku.py`
   - **DigitalOcean**: `sudo ./deploy_to_digitalocean.sh`
4. **Embed in Squarespace** using the provided code

---

## 🔧 **Repository Structure**

```
education-jobs-sourcing-tool/
├── app.py                          # Main Flask application
├── production_scraper.py           # Multi-page job scraper
├── auto_refresh_system.py          # Auto-refresh scheduler
├── deploy_to_heroku.py            # Heroku deployment script
├── deploy_to_digitalocean.sh      # DigitalOcean deployment script
├── requirements.txt               # Python dependencies
├── Procfile                       # Heroku configuration
├── templates/                     # HTML templates
│   ├── index.html
│   ├── admin_applications.html
│   ├── candidate_register.html
│   └── ...
├── uploads/                       # Resume storage
├── edjoin_jobs.json              # Job positions data
└── *.md                          # Documentation files
```

---

## 🎉 **Benefits of GitHub Upload**

✅ **Version Control** - Track all changes  
✅ **Backup** - Never lose your code  
✅ **Collaboration** - Share with team members  
✅ **Deployment** - Easy deployment from Git  
✅ **Documentation** - Professional README  
✅ **Issues** - Track bugs and features  
✅ **Releases** - Version your application  

**Your Education Jobs Sourcing Tool is now ready for professional deployment!** 🚀
