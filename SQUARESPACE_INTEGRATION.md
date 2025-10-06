# 🎨 Squarespace Integration Guide

## 🚀 Quick Integration (5 minutes)

### Step 1: Deploy Your App
First, deploy your app to get an external URL:
- **Heroku**: `https://your-app-name.herokuapp.com`
- **DigitalOcean**: `https://your-app-name.ondigitalocean.app`
- **Custom Domain**: `https://your-domain.com`

### Step 2: Add to Squarespace
1. **Go to your Squarespace site**
2. **Add a new page** or edit existing page
3. **Add a "Code Block"**
4. **Paste the embed code** (see below)
5. **Save and publish**

---

## 📱 Embed Codes for Squarespace

### Basic Embed (Recommended)

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

### Responsive Embed (Mobile-Optimized)

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

### Branded Integration (Matches Your Site)

```html
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px;
    border-radius: 12px;
    margin: 20px 0;
    text-align: center;
">
    <h2 style="color: white; margin-bottom: 10px; font-size: 2em;">
        🎓 Education Leadership Positions
    </h2>
    <p style="color: white; margin-bottom: 20px; font-size: 1.1em;">
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

### Minimal Integration (Clean Look)

```html
<div style="padding: 20px 0;">
    <iframe 
        src="https://your-domain.com/embed-enhanced" 
        width="100%" 
        height="800px" 
        frameborder="0"
        style="border: none;">
    </iframe>
</div>
```

---

## 🎯 Squarespace-Specific Instructions

### Method 1: Code Block (Easiest)

1. **Edit your page**
2. **Click "+" to add content**
3. **Select "Code"**
4. **Paste embed code**
5. **Save**

### Method 2: Full Page Integration

1. **Create new page**
2. **Add only the embed code**
3. **Make page full-width**
4. **Hide navigation if desired**

### Method 3: Sidebar Integration

1. **Add Code Block to sidebar**
2. **Use smaller height** (400-500px)
3. **Adjust width to fit sidebar**

---

## 🎨 Customization Options

### Match Your Brand Colors

```html
<style>
    .custom-jobs-widget {
        background: #YOUR_PRIMARY_COLOR;
        padding: 20px;
        border-radius: 8px;
    }
    
    .custom-jobs-widget h2 {
        color: #YOUR_TEXT_COLOR;
    }
</style>

<div class="custom-jobs-widget">
    <h2>Education Leadership Positions</h2>
    <iframe src="https://your-domain.com/embed-enhanced" width="100%" height="800px" frameborder="0"></iframe>
</div>
```

### Add Your Logo

```html
<div style="text-align: center; margin-bottom: 20px;">
    <img src="YOUR_LOGO_URL" alt="Your Logo" style="max-height: 60px;">
</div>
<iframe src="https://your-domain.com/embed-enhanced" width="100%" height="800px" frameborder="0"></iframe>
```

### Custom Header Text

```html
<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="color: #333; margin-bottom: 10px;">Find Your Next Leadership Role</h1>
    <p style="color: #666; font-size: 1.1em;">Connect with top education leadership positions across California</p>
</div>
<iframe src="https://your-domain.com/embed-enhanced" width="100%" height="800px" frameborder="0"></iframe>
```

---

## 📱 Mobile Optimization

### Responsive Design

The widget automatically adapts to mobile devices, but you can fine-tune:

```html
<style>
    .mobile-optimized {
        width: 100%;
        margin: 0;
        padding: 10px;
    }
    
    @media (max-width: 768px) {
        .mobile-optimized iframe {
            height: 600px;
        }
    }
    
    @media (max-width: 480px) {
        .mobile-optimized iframe {
            height: 500px;
        }
    }
</style>

<div class="mobile-optimized">
    <iframe src="https://your-domain.com/embed-enhanced" width="100%" height="800px" frameborder="0"></iframe>
</div>
```

---

## 🔧 Advanced Integration

### Multiple Widgets on Same Page

```html
<!-- Job Listings Widget -->
<div style="margin-bottom: 30px;">
    <h3>Current Openings</h3>
    <iframe src="https://your-domain.com/embed" width="100%" height="600px" frameborder="0"></iframe>
</div>

<!-- Candidate Registration Widget -->
<div>
    <h3>Join Our Talent Pool</h3>
    <iframe src="https://your-domain.com/candidate/register" width="100%" height="700px" frameborder="0"></iframe>
</div>
```

### Conditional Display

```html
<script>
// Show different widgets based on user type
function showWidget(userType) {
    const iframe = document.getElementById('jobs-widget');
    if (userType === 'candidate') {
        iframe.src = 'https://your-domain.com/embed-enhanced';
    } else {
        iframe.src = 'https://your-domain.com/embed';
    }
}
</script>

<iframe id="jobs-widget" src="https://your-domain.com/embed-enhanced" width="100%" height="800px" frameborder="0"></iframe>
```

---

## 🧪 Testing Your Integration

### Before Going Live

1. **Test on Desktop**: Verify widget displays correctly
2. **Test on Mobile**: Check responsive behavior
3. **Test Candidate Registration**: Ensure forms work
4. **Test Job Applications**: Verify apply buttons work
5. **Test Google Forms**: Confirm data submission

### Test Checklist

- [ ] Widget loads without errors
- [ ] All buttons and links work
- [ ] Forms submit successfully
- [ ] Google Forms receives data
- [ ] Mobile display is correct
- [ ] Branding matches your site

---

## 🚀 Quick Start Template

### Complete Integration Template

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .education-jobs-container {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .header-section {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
        }
        
        .widget-container {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        
        .widget-container iframe {
            width: 100%;
            height: 900px;
            border: none;
        }
        
        @media (max-width: 768px) {
            .widget-container iframe {
                height: 700px;
            }
        }
    </style>
</head>
<body>
    <div class="education-jobs-container">
        <div class="header-section">
            <h1>🎓 Education Leadership Positions</h1>
            <p>Discover director, dean, and assistant director positions from EdJoin.org</p>
        </div>
        
        <div class="widget-container">
            <iframe src="https://your-domain.com/embed-enhanced"></iframe>
        </div>
    </div>
</body>
</html>
```

---

## 📞 Support & Troubleshooting

### Common Issues

1. **Widget not loading**
   - Check iframe URL is correct
   - Verify HTTPS is enabled
   - Test URL in browser directly

2. **Styling conflicts**
   - Add `!important` to CSS rules
   - Use more specific selectors
   - Check Squarespace theme compatibility

3. **Mobile display issues**
   - Adjust iframe height for mobile
   - Test on actual devices
   - Use responsive CSS

### Getting Help

1. Test the widget URL directly in your browser
2. Check browser console for errors
3. Verify all URLs are accessible
4. Test on different devices and browsers

---

## 🎉 Final Result

Once integrated, your Squarespace site will have:

✅ **Professional Job Widget** - Beautiful, responsive design  
✅ **Candidate Registration** - Easy talent pool signup  
✅ **Real-time Job Data** - Live positions from EdJoin.org  
✅ **Google Forms Integration** - All data goes to your form  
✅ **Mobile Responsive** - Works on all devices  
✅ **Brand Consistent** - Matches your site design  

**Your Education Jobs Sourcing Tool will be live on your Squarespace website!** 🚀
