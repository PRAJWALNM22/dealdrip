# 💧 Dealdrip - Price Tracking Tool

A complete full-stack web application for tracking e-commerce product prices and receiving email notifications when prices drop below your target values.

## 🚀 Features

- **🔍 Universal Price Detection**: Works with major e-commerce sites (Amazon, eBay, etc.)
- **📧 Email Notifications**: Get instant alerts when prices drop
- **⏰ Automated Monitoring**: Daily price checks with background scheduler
- **🛡️ Secure & Private**: Your data stays local in SQLite database
- **📱 Responsive Design**: Beautiful, modern interface that works on all devices
- **🧪 Price Testing**: Test price extraction before setting up tracking

## 📋 Requirements

- Python 3.7 or higher
- Internet connection for price scraping and email notifications

## 🛠️ Installation & Setup

### 1. Clone or Download

If you have this as a zip file, extract it. Otherwise, navigate to the project directory:

```bash
cd C:\Users\ADMIN\Desktop\dealdrip
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Email Configuration (Required for Notifications)

For email notifications to work, you need to set environment variables for your email provider. Here are examples for Gmail:

#### Windows (PowerShell):
```powershell
$env:SMTP_SERVER = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:EMAIL_USER = "your-email@gmail.com"
$env:EMAIL_PASSWORD = "your-app-password"
```

#### Windows (Command Prompt):
```cmd
set SMTP_SERVER=smtp.gmail.com
set SMTP_PORT=587
set EMAIL_USER=your-email@gmail.com
set EMAIL_PASSWORD=your-app-password
```

#### macOS/Linux:
```bash
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export EMAIL_USER="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
```

### 4. Gmail App Password Setup (If Using Gmail)

1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account Settings → Security
3. Under "Signing in to Google," click "App passwords"
4. Generate a new app password for "Dealdrip"
5. Use this app password (not your regular Gmail password) in the `EMAIL_PASSWORD` variable

### 5. Alternative Email Providers

You can use other email providers by adjusting the environment variables:

#### Outlook/Hotmail:
```bash
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

#### Yahoo:
```bash
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

## 🏃 Running the Application

1. **Start the server:**
   ```bash
   python app.py
   ```

2. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

3. **You should see the Dealdrip interface!** 🎉

## 💻 Usage Guide

### Adding a Product for Tracking

1. **Enter Product URL**: Paste the full URL of the product page you want to track
2. **Set Target Price**: Enter the price you want to be notified at (in USD)
3. **Enter Email**: Your email address for notifications
4. **Test Price Extraction** (Optional): Click "Test Price Extraction" to verify the app can detect the current price
5. **Start Tracking**: Click "💧 Start Dripping" to begin monitoring

### Supported Websites

The application works with most major e-commerce sites, including:
- Amazon
- eBay  
- Walmart
- Best Buy
- Target
- And many others that display prices in standard formats

### Price Checking Schedule

- **Automatic**: Prices are checked daily at 9:00 AM
- **Manual**: You can trigger manual checks via the API endpoint `/api/manual-check`

## 🔧 API Endpoints

The application provides several API endpoints:

### `POST /api/track`
Add a new product for price tracking.

**Request Body:**
```json
{
    "url": "https://www.amazon.com/product-page",
    "target_price": 50.00,
    "email": "user@example.com"
}
```

### `POST /api/test-price`
Test price extraction from a URL.

**Request Body:**
```json
{
    "url": "https://www.amazon.com/product-page"
}
```

### `POST /api/manual-check`
Manually trigger price checking for all active alerts.

## 🗄️ Database

The application uses SQLite to store tracking data locally in `dealdrip.db`. The database includes:

- Product URLs
- Target prices
- User emails
- Current prices
- Last check timestamps
- Alert status

## 📧 Email Notifications

When a price drops to or below your target price, you'll receive a beautiful HTML email notification containing:

- Current price vs. target price
- Direct link to the product
- "Buy Now" button
- Professional formatting

## 🛡️ Troubleshooting

### Common Issues

1. **"Could not extract price"**
   - The website might have changed its layout
   - Try the "Test Price Extraction" feature first
   - Some sites might block automated requests

2. **Email notifications not working**
   - Verify your environment variables are set correctly
   - For Gmail, ensure you're using an App Password, not your regular password
   - Check that 2FA is enabled on your Gmail account

3. **Application won't start**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check that Python 3.7+ is installed: `python --version`

### Advanced Configuration

#### Changing the Schedule
To modify when price checks occur, edit line 339-345 in `app.py`:

```python
scheduler.add_job(
    func=check_prices,
    trigger=CronTrigger(hour=9, minute=0),  # 9:00 AM daily
    id='daily_price_check',
    name='Check prices daily',
    replace_existing=True
)
```

#### Testing Mode
For testing, uncomment lines 347-354 in `app.py` to enable price checking every 5 minutes:

```python
scheduler.add_job(
    func=check_prices,
    trigger='interval',
    minutes=5,
    id='test_price_check',
    name='Test price check every 5 minutes'
)
```

## 🔐 Privacy & Security

- All data is stored locally on your machine
- No data is sent to external servers (except for price scraping and email notifications)
- Email credentials are only used for sending notifications
- The application respects website robots.txt files when possible

## 📁 Project Structure

```
dealdrip/
├── app.py                 # Main Flask application
├── index.html            # Frontend interface
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── dealdrip.db          # SQLite database (created automatically)
```

## 🔄 Updates & Maintenance

### Updating Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Backup Your Data
To backup your tracking data:
```bash
# Copy the database file
cp dealdrip.db dealdrip_backup.db
```

## 🤝 Contributing

This is a complete, self-contained application. Feel free to modify and enhance it for your needs!

### Potential Improvements
- Add more sophisticated price extraction algorithms
- Support for different currencies
- Web dashboard for managing tracked products
- Integration with messaging services (SMS, Slack, etc.)
- Historical price tracking and charts

## 📜 License

This project is open source and available under the MIT License.

## ❓ Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify all environment variables are set correctly
3. Ensure all dependencies are properly installed
4. Check the console output for error messages

---

**Happy deal hunting! 💧🛒**