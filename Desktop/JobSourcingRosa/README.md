# Education Jobs Sourcing Tool

A comprehensive tool for sourcing and displaying education leadership positions from EdJoin.org, with resume upload functionality and Google Sheets integration.

## Features

- **Automated Scraping**: Scrapes director, dean, assistant director, and principal positions from EdJoin.org
- **Google Sheets Integration**: Automatically saves scraped data to Google Sheets
- **Web Dashboard**: Beautiful, responsive web interface to display positions
- **Resume Upload**: Candidates can apply directly through the website
- **Embeddable Widget**: Easy integration into external websites
- **Admin Panel**: View and manage job applications

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Google Sheets (Optional)

1. Create a Google Cloud Project
2. Enable the Google Sheets API
3. Create a service account and download the JSON key
4. Rename the key file to `service_account.json` and place it in the project root
5. Create a Google Sheet and share it with the service account email

### 3. Run the Scraper

```bash
python edjoin_scraper.py
```

This will:
- Scrape positions from EdJoin.org
- Save data to `edjoin_jobs.json`
- Upload to Google Sheets (if configured)

### 4. Start the Web Application

```bash
python app.py
```

Visit `http://localhost:5000` to see the dashboard.

## Usage

### Scraping Jobs

The scraper targets these roles:
- Director
- Assistant Director
- Dean
- Principal
- Superintendent

Run the scraper manually or set up automated scheduling:

```bash
# Manual run
python edjoin_scraper.py

# Schedule with cron (daily at 6 AM)
0 6 * * * cd /path/to/project && python edjoin_scraper.py
```

### Web Dashboard

The dashboard provides:
- **Job Listings**: View all scraped positions
- **Filtering**: Filter by role type
- **Application System**: Candidates can apply with resume upload
- **Admin Panel**: View and manage applications

### Embedding in External Websites

Use the embed widget on any website:

```html
<iframe src="http://your-domain.com/embed" 
        width="100%" 
        height="600px" 
        frameborder="0">
</iframe>
```

## File Structure

```
JobSourcingRosa/
├── app.py                 # Flask web application
├── edjoin_scraper.py     # EdJoin.org scraper
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── apply.html
│   ├── embed.html
│   └── admin_applications.html
├── uploads/              # Resume uploads directory
├── edjoin_jobs.json     # Scraped job data
├── applications.json    # Job applications
└── service_account.json # Google Sheets credentials
```

## Configuration

### Environment Variables

Create a `.env` file:

```env
GOOGLE_SHEET_NAME=EdJoin Education Jobs
SERVICE_ACCOUNT_FILE=service_account.json
FLASK_SECRET_KEY=your-secret-key
FLASK_DEBUG=True
MAX_PAGES_PER_ROLE=10
SCRAPING_DELAY=2
```

### Google Sheets Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable the Google Sheets API
4. Create credentials (Service Account)
5. Download the JSON key file
6. Rename to `service_account.json`
7. Create a Google Sheet and share with the service account email

## Deployment

### Local Development

```bash
python app.py
```

### Production Deployment

1. **Heroku**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   heroku create your-app-name
   git push heroku main
   ```

2. **DigitalOcean App Platform**:
   - Connect your GitHub repository
   - Set environment variables
   - Deploy automatically

3. **VPS/Server**:
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Run with Gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   
   # Set up Nginx reverse proxy
   # Configure SSL certificate
   ```

## Scheduling

### Cron Job (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add daily scraping at 6 AM
0 6 * * * cd /path/to/JobSourcingRosa && python edjoin_scraper.py
```

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to daily at 6 AM
4. Set action to run `python edjoin_scraper.py`

## API Endpoints

- `GET /` - Main dashboard
- `GET /api/jobs` - JSON API for all jobs
- `GET /api/jobs/<role>` - JSON API for specific role
- `GET /embed` - Embeddable widget
- `GET /apply/<job_index>` - Job application form
- `GET /admin/applications` - Admin panel

## Troubleshooting

### Common Issues

1. **Scraping fails**: EdJoin.org may have changed their HTML structure
2. **Google Sheets error**: Check service account permissions
3. **File upload issues**: Ensure uploads directory exists and has write permissions

### Debug Mode

Enable debug mode in `config.py`:

```python
DEBUG = True
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in the console
3. Open an issue on GitHub

## Future Enhancements

- [ ] Email notifications for new positions
- [ ] Advanced search and filtering
- [ ] Resume parsing and keyword matching
- [ ] Integration with more job boards
- [ ] Analytics dashboard
- [ ] Mobile app
