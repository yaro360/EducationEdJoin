# Installation Guide

## Quick Start (5 minutes)

### 1. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Run the Application

```bash
python3 run.py
```

Choose option 3 to run scraper + start web app.

### 3. Open Your Browser

Visit: http://localhost:5000

## What You Get

✅ **Complete Job Sourcing Tool** with:
- Automated scraping from EdJoin.org
- Beautiful web dashboard
- Resume upload system
- Google Sheets integration
- Embeddable widget for external sites

## Features Overview

### 🎯 Targeted Positions
- Director
- Assistant Director  
- Dean
- Principal
- Superintendent

### 📊 Dashboard Features
- Live job listings
- Role-based filtering
- Application system
- Admin panel for managing applications

### 🔗 Easy Integration
- Embed widget on any website
- JSON API endpoints
- Google Sheets sync

## Next Steps

1. **Set up Google Sheets** (optional):
   ```bash
   python3 setup_google_sheets.py
   ```

2. **Schedule automatic scraping**:
   ```bash
   python3 scheduler.py
   ```

3. **Deploy to production**:
   - Heroku
   - DigitalOcean
   - AWS
   - Any VPS

## File Structure

```
JobSourcingRosa/
├── app.py                    # Main web application
├── edjoin_scraper.py        # Job scraper
├── run.py                   # Easy startup script
├── test_app.py              # Test the application
├── scheduler.py             # Automated scheduling
├── setup_google_sheets.py   # Google Sheets setup
├── requirements.txt         # Dependencies
├── README.md               # Full documentation
├── templates/              # Web pages
└── uploads/                # Resume storage
```

## Troubleshooting

**Dependencies not found?**
```bash
pip3 install requests beautifulsoup4 flask gspread google-auth
```

**Permission denied?**
```bash
chmod +x run.py
```

**Port already in use?**
Change port in `app.py` line 95: `app.run(debug=True, host='0.0.0.0', port=5001)`

## Support

- Check `README.md` for detailed documentation
- Run `python3 test_app.py` to test the setup
- All code is well-commented and documented

---

**Ready to source education jobs? Run `python3 run.py` and get started!** 🚀

