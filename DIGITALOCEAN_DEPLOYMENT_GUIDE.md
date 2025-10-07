# 🚀 DigitalOcean App Platform Deployment Guide

## 📋 Prerequisites

1. **DigitalOcean Account** - Sign up at [digitalocean.com](https://digitalocean.com)
2. **DigitalOcean CLI (doctl)** - Install the command-line tool
3. **GitHub Repository** - Your code is already at `yaro360/EducationEdJoin`

## 🔧 Setup Steps

### 1. Install DigitalOcean CLI

```bash
# On macOS
brew install doctl

# On Linux/Windows
# Visit: https://docs.digitalocean.com/reference/doctl/how-to/install/
```

### 2. Authenticate with DigitalOcean

```bash
doctl auth init
```

This will open a browser window where you can:
- Log in to your DigitalOcean account
- Generate an API token
- Copy the token back to your terminal

### 3. Deploy Your Application

```bash
python3 deploy_to_digitalocean.py
```

## 💰 Pricing

- **Basic Plan**: $5/month
- **Includes**: 1 app, 1 service, 512MB RAM
- **Perfect for**: Your education jobs dashboard

## 🌐 What Happens After Deployment

1. **App URL**: `https://education-jobs-dashboard-xxxxx.ondigitalocean.app`
2. **Automatic Deploys**: Every time you push to GitHub
3. **Scraper Job**: Runs automatically to update job listings
4. **Environment Variables**: Set in DigitalOcean dashboard

## ⚙️ Configuration

### Environment Variables to Set:
- `FLASK_ENV=production`
- `SECRET_KEY=your-super-secret-key`
- `GOOGLE_FORMS_URL=your-google-form-url`
- `GOOGLE_FORMS_ENTRY_*` (for form field mapping)

### Google Forms Setup:
1. Create a Google Form for candidate registration
2. Get the form submission URL
3. Map form fields to environment variables
4. Set variables in DigitalOcean dashboard

## 🔄 Automatic Updates

The scraper will run automatically to:
- Update job listings every 24 hours
- Scrape all pages from EdJoin.org
- Save data to Google Sheets
- Update the web dashboard

## 📱 Squarespace Integration

Once deployed, you can embed your dashboard using:
```html
<iframe src="https://your-app-url.ondigitalocean.app/embed-enhanced" 
        width="100%" 
        height="600" 
        frameborder="0">
</iframe>
```

## 🆘 Troubleshooting

### Common Issues:
1. **doctl not found**: Install with `brew install doctl`
2. **Authentication failed**: Run `doctl auth init`
3. **Deployment failed**: Check GitHub repository permissions
4. **App not loading**: Check environment variables

### Support:
- DigitalOcean Documentation: [docs.digitalocean.com](https://docs.digitalocean.com)
- App Platform Guide: [DigitalOcean App Platform](https://docs.digitalocean.com/products/app-platform/)

## 🎯 Next Steps

1. Run the deployment script
2. Wait for deployment to complete
3. Test your application
4. Configure Google Forms
5. Embed in Squarespace
6. Set up monitoring and alerts

---

**Ready to deploy?** Run: `python3 deploy_to_digitalocean.py` 🚀

