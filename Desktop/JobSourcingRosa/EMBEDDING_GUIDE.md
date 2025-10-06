# Embedding Guide - Education Jobs Widget

## 🚀 Quick Embedding Options

### Option 1: Simple Iframe (Easiest)

Add this code to any website:

```html
<iframe 
    src="http://your-domain.com/embed" 
    width="100%" 
    height="800px" 
    frameborder="0"
    style="border: none; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
</iframe>
```

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

### Option 3: Custom Styled Widget

```html
<div style="width: 100%; max-width: 1200px; margin: 0 auto;">
    <iframe 
        src="http://your-domain.com/embed" 
        width="100%" 
        height="700px" 
        frameborder="0"
        style="border: none; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
    </iframe>
</div>
```

## 🎯 Platform-Specific Instructions

### WordPress
1. Go to your page/post editor
2. Switch to "Text" or "HTML" mode
3. Paste the iframe code where you want the widget
4. Publish/Update the page

### Squarespace
1. Add a "Code Block" to your page
2. Paste the iframe code
3. Save the block

### Wix
1. Add an "Embed" element
2. Choose "Custom Code"
3. Paste the iframe code
4. Adjust size as needed

### Shopify
1. Go to Online Store > Themes
2. Edit your theme
3. Add the iframe code to your desired template
4. Save changes

### Custom HTML/CSS
```html
<!DOCTYPE html>
<html>
<head>
    <title>Education Jobs</title>
    <style>
        .jobs-widget {
            width: 100%;
            max-width: 1200px;
            margin: 20px auto;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="jobs-widget">
        <iframe 
            src="http://your-domain.com/embed" 
            width="100%" 
            height="800px" 
            frameborder="0">
        </iframe>
    </div>
</body>
</html>
```

## 🔧 Advanced Integration

### JavaScript API Integration

```javascript
// Fetch jobs data
fetch('http://your-domain.com/api/jobs')
    .then(response => response.json())
    .then(jobs => {
        // Display jobs in your custom layout
        displayJobs(jobs);
    });

// Fetch candidate matches
fetch('http://your-domain.com/api/candidate-matches/candidate_id')
    .then(response => response.json())
    .then(matches => {
        // Display matches
        displayMatches(matches);
    });
```

### React Component

```jsx
import React, { useState, useEffect } from 'react';

const EducationJobsWidget = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://your-domain.com/api/jobs')
            .then(response => response.json())
            .then(data => {
                setJobs(data);
                setLoading(false);
            });
    }, []);

    if (loading) return <div>Loading...</div>;

    return (
        <div className="jobs-widget">
            {jobs.map(job => (
                <div key={job.url} className="job-card">
                    <h3>{job.title}</h3>
                    <p>{job.role} - {job.location}</p>
                    <a href={job.url} target="_blank">View Job</a>
                </div>
            ))}
        </div>
    );
};

export default EducationJobsWidget;
```

### Vue.js Component

```vue
<template>
    <div class="jobs-widget">
        <div v-for="job in jobs" :key="job.url" class="job-card">
            <h3>{{ job.title }}</h3>
            <p>{{ job.role }} - {{ job.location }}</p>
            <a :href="job.url" target="_blank">View Job</a>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            jobs: []
        }
    },
    async mounted() {
        const response = await fetch('http://your-domain.com/api/jobs');
        this.jobs = await response.json();
    }
}
</script>
```

## 📱 Responsive Design

### Mobile-Optimized Embedding

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
    
    @media (max-width: 480px) {
        .jobs-widget {
            height: 400px;
        }
    }
</style>

<div class="jobs-widget">
    <iframe 
        src="http://your-domain.com/embed" 
        width="100%" 
        height="100%" 
        frameborder="0">
    </iframe>
</div>
```

## 🎨 Custom Styling

### Branded Widget

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
        src="http://your-domain.com/embed" 
        width="100%" 
        height="700px" 
        frameborder="0"
        style="border-radius: 8px; background: white;">
    </iframe>
</div>
```

## 🔗 API Endpoints

### Available Endpoints

- `GET /api/jobs` - All job positions
- `GET /api/jobs/<role>` - Jobs filtered by role
- `GET /api/candidate-matches/<candidate_id>` - Candidate matches
- `GET /api/job-candidates/<job_url>` - Top candidates for a job
- `POST /candidate/register` - Register new candidate

### Example API Usage

```javascript
// Get all jobs
const jobs = await fetch('http://your-domain.com/api/jobs').then(r => r.json());

// Get director positions only
const directors = await fetch('http://your-domain.com/api/jobs/director').then(r => r.json());

// Register a candidate
const candidate = await fetch('http://your-domain.com/candidate/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: 'John Doe',
        email: 'john@example.com',
        preferred_roles: ['Director', 'Assistant Director']
    })
}).then(r => r.json());
```

## 🚀 Deployment Options

### 1. Heroku (Free)
```bash
# Deploy to Heroku
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
git push heroku main
```

### 2. DigitalOcean App Platform
1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically

### 3. VPS/Server
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Set up Nginx reverse proxy
# Configure SSL certificate
```

## 🔧 Customization

### Custom Domain
1. Point your domain to your server
2. Update iframe URLs to use your domain
3. Configure SSL certificate

### Custom Branding
1. Edit templates in `/templates/` folder
2. Update colors, logos, and styling
3. Redeploy the application

### Additional Features
1. Add email notifications
2. Integrate with your CRM
3. Add analytics tracking
4. Customize matching algorithm

## 📞 Support

For embedding help:
1. Check the browser console for errors
2. Verify the iframe URL is accessible
3. Test on different devices and browsers
4. Contact support with specific error messages

## 🎯 Best Practices

1. **Always use HTTPS** for production
2. **Test on mobile devices** - the widget is responsive
3. **Monitor performance** - large iframes can slow page load
4. **Update regularly** - the widget shows live data
5. **Customize styling** to match your brand
6. **Use the enhanced widget** for better candidate engagement

---

**Ready to embed? Choose your preferred method and start showcasing education leadership positions on your website!** 🚀
