#!/bin/bash

# DigitalOcean Deployment Script for Education Jobs Sourcing Tool
# Run this script on your DigitalOcean droplet

set -e

echo "🚀 Education Jobs Sourcing Tool - DigitalOcean Deployment"
echo "========================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}🔄 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root (use sudo)"
    exit 1
fi

# Get domain name
read -p "Enter your domain name (or press Enter for IP address): " DOMAIN_NAME
if [ -z "$DOMAIN_NAME" ]; then
    DOMAIN_NAME=$(curl -s ifconfig.me)
    print_warning "Using IP address: $DOMAIN_NAME"
fi

print_status "Starting deployment for domain: $DOMAIN_NAME"

# Update system
print_status "Updating system packages..."
apt update && apt upgrade -y

# Install required packages
print_status "Installing required packages..."
apt install -y python3 python3-pip python3-venv nginx git curl wget unzip

# Create app directory
print_status "Creating application directory..."
mkdir -p /var/www/education-jobs
cd /var/www/education-jobs

# Clone repository (replace with your actual repository URL)
print_status "Cloning repository..."
if [ ! -d ".git" ]; then
    # If no git repo, create one and copy files
    git init
    # You'll need to copy your files here or clone from a repository
    print_warning "Please copy your project files to /var/www/education-jobs/"
    print_warning "Or set up a Git repository and clone it here"
    read -p "Press Enter when files are in place..."
fi

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p uploads
mkdir -p logs
chmod 755 uploads
chmod 755 logs

# Create systemd service file
print_status "Creating systemd service..."
cat > /etc/systemd/system/education-jobs.service << EOF
[Unit]
Description=Education Jobs Sourcing Tool
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/education-jobs
Environment=PATH=/var/www/education-jobs/venv/bin
ExecStart=/var/www/education-jobs/venv/bin/gunicorn --bind 127.0.0.1:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx configuration
print_status "Creating Nginx configuration..."
cat > /etc/nginx/sites-available/education-jobs << EOF
server {
    listen 80;
    server_name $DOMAIN_NAME;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Main application
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # File uploads
    location /uploads/ {
        alias /var/www/education-jobs/uploads/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header X-Content-Type-Options nosniff;
    }

    # Static files
    location /static/ {
        alias /var/www/education-jobs/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Health check
    location /health {
        proxy_pass http://127.0.0.1:5000/health;
        access_log off;
    }
}
EOF

# Enable Nginx site
print_status "Enabling Nginx site..."
ln -sf /etc/nginx/sites-available/education-jobs /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
print_status "Testing Nginx configuration..."
nginx -t

# Set proper permissions
print_status "Setting file permissions..."
chown -R www-data:www-data /var/www/education-jobs
chmod -R 755 /var/www/education-jobs

# Enable and start services
print_status "Starting services..."
systemctl daemon-reload
systemctl enable education-jobs
systemctl start education-jobs
systemctl enable nginx
systemctl restart nginx

# Set up auto-refresh cron job
print_status "Setting up auto-refresh cron job..."
(crontab -l 2>/dev/null; echo "0 6 * * * cd /var/www/education-jobs && /var/www/education-jobs/venv/bin/python production_scraper.py >> /var/log/job_refresh.log 2>&1") | crontab -

# Install SSL certificate (optional)
read -p "Do you want to install SSL certificate with Let's Encrypt? (y/n): " INSTALL_SSL
if [ "$INSTALL_SSL" = "y" ] || [ "$INSTALL_SSL" = "Y" ]; then
    print_status "Installing SSL certificate..."
    apt install -y certbot python3-certbot-nginx
    certbot --nginx -d $DOMAIN_NAME --non-interactive --agree-tos --email admin@$DOMAIN_NAME
    print_success "SSL certificate installed!"
fi

# Run initial job scraper
print_status "Running initial job scraper..."
cd /var/www/education-jobs
source venv/bin/activate
python3 production_scraper.py

# Check service status
print_status "Checking service status..."
systemctl status education-jobs --no-pager

# Display results
echo ""
echo "🎉 Deployment completed successfully!"
echo "=================================="
echo "🌐 Your app is live at: http://$DOMAIN_NAME"
echo ""
echo "📋 Available URLs:"
echo "   Main Dashboard: http://$DOMAIN_NAME"
echo "   Embed Widget: http://$DOMAIN_NAME/embed-enhanced"
echo "   Admin Panel: http://$DOMAIN_NAME/admin/applications"
echo "   Health Check: http://$DOMAIN_NAME/health"
echo ""
echo "🔗 Squarespace Embed Code:"
echo ""
cat << EOF
<div id="education-jobs-widget">
    <iframe 
        src="http://$DOMAIN_NAME/embed-enhanced" 
        width="100%" 
        height="800" 
        frameborder="0"
        style="border: none; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    </iframe>
</div>
EOF
echo ""
echo "🎯 Next Steps:"
echo "1. Copy the embed code above to your Squarespace site"
echo "2. Test the job board functionality"
echo "3. Customize the styling to match your brand"
echo "4. Set up monitoring and backups"
echo ""
echo "📊 Monitoring Commands:"
echo "   View logs: journalctl -u education-jobs -f"
echo "   Check status: systemctl status education-jobs"
echo "   Restart service: systemctl restart education-jobs"
echo ""
echo "🚀 Your Education Jobs Sourcing Tool is now live!"

# Create a simple monitoring script
cat > /var/www/education-jobs/monitor.sh << 'EOF'
#!/bin/bash
# Simple monitoring script

echo "🔍 Education Jobs Sourcing Tool - Status Check"
echo "=============================================="

echo "📊 Service Status:"
systemctl is-active education-jobs

echo ""
echo "📈 Recent Logs:"
journalctl -u education-jobs --since "1 hour ago" --no-pager | tail -10

echo ""
echo "💾 Disk Usage:"
df -h /var/www/education-jobs

echo ""
echo "🌐 Health Check:"
curl -s http://localhost:5000/health | python3 -m json.tool 2>/dev/null || echo "Health check failed"
EOF

chmod +x /var/www/education-jobs/monitor.sh

print_success "Monitoring script created at /var/www/education-jobs/monitor.sh"
print_success "Run './monitor.sh' to check system status"
