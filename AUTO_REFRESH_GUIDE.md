# 🔄 Automatic Job Refresh System

## 🎯 Overview

Your Education Jobs Sourcing Tool now has **multiple ways to automatically refresh job positions** every 24 hours (or any interval you prefer). Here are all the options:

---

## 🚀 **Option 1: Python Scheduler (Recommended for Development)**

### **How it works:**
- Runs continuously in the background
- Automatically refreshes jobs every 24 hours at 6 AM
- Handles errors gracefully
- Logs all activities

### **Setup:**
```bash
# Install required package
pip install schedule

# Run the scheduler
python3 auto_refresh_system.py
```

### **Features:**
- ✅ **Daily at 6 AM** - Perfect timing for fresh morning data
- ✅ **30-minute timeout** - Prevents hanging
- ✅ **Error handling** - Continues running even if refresh fails
- ✅ **Detailed logging** - Track all activities
- ✅ **Manual refresh** - Can trigger immediate refresh

---

## 🕐 **Option 2: Cron Job (Recommended for Production)**

### **How it works:**
- Uses system-level scheduling
- Runs independently of your app
- Most reliable for production servers

### **Setup:**
```bash
# 1. Create the cron job script
python3 auto_refresh_system.py
# Choose option 2 when prompted

# 2. Edit your crontab
crontab -e

# 3. Add this line (runs daily at 6 AM):
0 6 * * * /Users/yco/Desktop/JobSourcingRosa/run_job_refresh.sh

# 4. Save and exit
```

### **Alternative Cron Schedules:**
```bash
# Every 12 hours
0 */12 * * * /path/to/run_job_refresh.sh

# Every 6 hours
0 */6 * * * /path/to/run_job_refresh.sh

# Every hour
0 * * * * /path/to/run_job_refresh.sh

# Weekdays only at 6 AM
0 6 * * 1-5 /path/to/run_job_refresh.sh

# Every Monday, Wednesday, Friday at 6 AM
0 6 * * 1,3,5 /path/to/run_job_refresh.sh
```

---

## 🐧 **Option 3: Systemd Service (Linux Servers)**

### **How it works:**
- Professional service management
- Automatic restart on failure
- System-level integration

### **Setup:**
```bash
# 1. Create the service file
python3 auto_refresh_system.py
# Choose option 3 when prompted

# 2. Install the service
sudo cp education-jobs-refresh.service /etc/systemd/system/

# 3. Enable and start
sudo systemctl enable education-jobs-refresh
sudo systemctl start education-jobs-refresh

# 4. Check status
sudo systemctl status education-jobs-refresh
```

---

## 🎮 **Option 4: Manual Refresh (Admin Panel)**

### **How it works:**
- Click "Refresh Jobs" button in admin panel
- Instant refresh of all positions
- Perfect for testing and immediate updates

### **Access:**
1. Go to: `http://localhost:5001/admin/applications`
2. Click **"Refresh Jobs"** button
3. Wait for completion (up to 30 minutes)
4. Page automatically reloads with new data

---

## ⚙️ **Configuration Options**

### **Refresh Intervals:**
```python
# In auto_refresh_system.py, you can change:

# Every 24 hours at 6 AM (default)
schedule.every().day.at("06:00").do(self.run_job_scraper)

# Every 12 hours
schedule.every(12).hours.do(self.run_job_scraper)

# Every 6 hours
schedule.every(6).hours.do(self.run_job_scraper)

# Every hour
schedule.every().hour.do(self.run_job_scraper)

# Every 30 minutes
schedule.every(30).minutes.do(self.run_job_scraper)
```

### **Timeout Settings:**
```python
# In app.py refresh_jobs() function:
timeout=1800  # 30 minutes (current)
timeout=3600  # 1 hour
timeout=900   # 15 minutes
```

---

## 📊 **Monitoring & Logs**

### **Log Files:**
- **`job_refresh.log`** - All refresh activities
- **Console output** - Real-time status
- **Admin panel** - Success/error messages

### **Log Examples:**
```
2025-10-06 12:30:00 - INFO - 🔄 Starting scheduled job refresh...
2025-10-06 12:30:15 - INFO - ✅ Job refresh completed successfully!
2025-10-06 12:30:15 - INFO - 📊 Found 29 total positions
2025-10-06 12:30:15 - INFO -    Director: 8 positions
2025-10-06 12:30:15 - INFO -    Assistant Director: 6 positions
```

### **Status API:**
```bash
# Check current status
curl http://localhost:5001/api/refresh-status

# Response:
{
  "total_positions": 29,
  "last_update": "2025-10-06T12:30:15.123456",
  "status": "success"
}
```

---

## 🚀 **Production Deployment**

### **For Heroku:**
```bash
# Add to Procfile:
web: gunicorn app:app
scheduler: python3 auto_refresh_system.py

# Deploy both processes
heroku ps:scale web=1 scheduler=1
```

### **For DigitalOcean/VPS:**
```bash
# Use cron job (recommended)
crontab -e
# Add: 0 6 * * * /path/to/run_job_refresh.sh

# Or use systemd service
sudo systemctl enable education-jobs-refresh
```

### **For Docker:**
```dockerfile
# Add to Dockerfile:
CMD ["sh", "-c", "python3 auto_refresh_system.py & python3 app.py"]
```

---

## 🔧 **Troubleshooting**

### **Common Issues:**

1. **"Permission denied" on cron job:**
   ```bash
   chmod +x run_job_refresh.sh
   ```

2. **"Command not found" in cron:**
   ```bash
   # Use full paths in cron
   0 6 * * * /usr/bin/python3 /full/path/to/production_scraper.py
   ```

3. **Scheduler stops running:**
   ```bash
   # Check logs
   tail -f job_refresh.log
   
   # Restart scheduler
   python3 auto_refresh_system.py
   ```

4. **Jobs not updating:**
   - Check if `edjoin_jobs.json` file exists
   - Verify file permissions
   - Check scraper logs for errors

### **Debug Mode:**
```bash
# Run with verbose logging
python3 auto_refresh_system.py

# Check specific scraper
python3 production_scraper.py

# Test manual refresh
curl -X POST http://localhost:5001/admin/refresh-jobs
```

---

## 📈 **Expected Results**

### **With Automatic Refresh:**
- ✅ **Fresh positions daily** - Always up-to-date
- ✅ **No manual intervention** - Fully automated
- ✅ **Error recovery** - Continues running even if one refresh fails
- ✅ **Scalable** - Can handle hundreds of positions
- ✅ **Reliable** - Multiple fallback methods

### **Performance:**
- **Refresh time**: 5-30 minutes (depending on EdJoin.org response)
- **Memory usage**: Minimal (runs in background)
- **CPU usage**: Low (only during refresh)
- **Storage**: ~1MB per 100 positions

---

## 🎯 **Recommended Setup**

### **For Development:**
```bash
# Use Python scheduler
python3 auto_refresh_system.py
```

### **For Production:**
```bash
# Use cron job
crontab -e
# Add: 0 6 * * * /path/to/run_job_refresh.sh
```

### **For Testing:**
```bash
# Use manual refresh
# Go to admin panel and click "Refresh Jobs"
```

---

## 🎉 **Summary**

**Your Education Jobs Sourcing Tool now has:**

✅ **4 different refresh methods** - Choose what works best  
✅ **Automatic daily updates** - Fresh positions every 24 hours  
✅ **Manual refresh option** - Instant updates when needed  
✅ **Error handling** - Continues running even if refresh fails  
✅ **Detailed logging** - Track all activities  
✅ **Production ready** - Deploy and scale immediately  
✅ **Flexible scheduling** - Any interval you prefer  

**Your job positions will now stay fresh and up-to-date automatically!** 🚀

