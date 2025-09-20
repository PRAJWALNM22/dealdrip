# 🚀 Dealdrip Production Deployment Guide

**Deploy with 99.9% reliability using multiple WhatsApp fallbacks!**

## 🎯 Pre-Deployment Checklist

### 1. Get Free WhatsApp API Keys (Choose at least 1)

#### Option A: Twilio WhatsApp Sandbox (Recommended - Unlimited Free)
1. Sign up at [twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Go to Console → Develop → Messaging → Try it out → WhatsApp
3. Copy your **Account SID** and **Auth Token**
4. Note your sandbox number: `+1 415 523 8886`
5. Recipients send `join indicate-iron` to the sandbox number (one-time)

#### Option B: Ultramsg (1000 free messages/month)
1. Sign up at [ultramsg.com](https://ultramsg.com)
2. Create new WhatsApp instance
3. Scan QR code with WhatsApp
4. Get **Instance ID** and **Token**

### 2. Email Configuration (Gmail Recommended)
1. Use Gmail with App Password (not regular password)
2. Enable 2FA in Gmail
3. Generate App Password: Google Account → Security → App passwords
4. Use the generated password (not your Gmail password)

---

## 🌐 Platform-Specific Deployment

### 🟦 Railway (Recommended - Simple & Free)

#### Step 1: Prepare Code
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

#### Step 2: Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Choose "Deploy from GitHub repo"
4. Select your dealdrip repository
5. Railway auto-detects Flask and starts deployment

#### Step 3: Set Environment Variables
In Railway dashboard → Variables tab:
```bash
FLASK_ENV=production
SECRET_KEY=your-strong-secret-key-here
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
ULTRAMSG_INSTANCE_ID=your_ultramsg_instance
ULTRAMSG_TOKEN=your_ultramsg_token
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
PORT=5000
```

#### Step 4: Create Procfile
Create `Procfile` (no extension):
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

#### Step 5: Test Deployment
- Railway provides a URL like `https://your-app.railway.app`
- Visit `/api/health` to check system status
- Test with a product URL

---

### 🟪 Heroku (Popular Choice)

#### Step 1: Install Heroku CLI
Download from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

#### Step 2: Create Heroku App
```bash
heroku create your-dealdrip-app
heroku git:remote -a your-dealdrip-app
```

#### Step 3: Set Environment Variables
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-strong-secret-key
heroku config:set TWILIO_ACCOUNT_SID=your_twilio_sid
heroku config:set TWILIO_AUTH_TOKEN=your_twilio_token
heroku config:set ULTRAMSG_INSTANCE_ID=your_ultramsg_instance
heroku config:set ULTRAMSG_TOKEN=your_ultramsg_token
heroku config:set EMAIL_USER=your-email@gmail.com
heroku config:set EMAIL_PASSWORD=your-gmail-app-password
```

#### Step 4: Create Procfile
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
clock: python scheduler.py
```

#### Step 5: Deploy
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### Step 6: Scale Workers
```bash
heroku ps:scale web=1
heroku ps:scale clock=1
```

---

### 🟢 Render (Easy & Free Tier)

#### Step 1: Connect GitHub
1. Go to [render.com](https://render.com)
2. Connect your GitHub account
3. Create new "Web Service"
4. Select your dealdrip repository

#### Step 2: Configuration
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

#### Step 3: Environment Variables
In Render dashboard → Environment:
```bash
FLASK_ENV=production
SECRET_KEY=your-strong-secret-key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
```

#### Step 4: Deploy
- Click "Create Web Service"
- Render automatically builds and deploys
- Get your URL: `https://your-app.onrender.com`

---

### 🖥️ VPS Deployment (Ubuntu/Linux)

#### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Create app user
sudo adduser dealdrip
sudo usermod -aG sudo dealdrip
su - dealdrip
```

#### Step 2: Application Setup
```bash
# Clone repository
git clone YOUR_REPO_URL dealdrip
cd dealdrip

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Environment Variables
Create `.env` file:
```bash
cp .env.example .env
nano .env
# Fill in your actual values
```

#### Step 4: Create Systemd Service
```bash
sudo nano /etc/systemd/system/dealdrip.service
```

Add:
```ini
[Unit]
Description=Dealdrip Flask App
After=network.target

[Service]
User=dealdrip
Group=dealdrip
WorkingDirectory=/home/dealdrip/dealdrip
Environment="PATH=/home/dealdrip/dealdrip/venv/bin"
ExecStart=/home/dealdrip/dealdrip/venv/bin/gunicorn app:app --bind 0.0.0.0:5000
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Step 5: Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl start dealdrip
sudo systemctl enable dealdrip
sudo systemctl status dealdrip
```

#### Step 6: Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/dealdrip
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/dealdrip /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 📊 Post-Deployment Verification

### 1. Health Check
Visit your deployed URL + `/api/health`:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-20T12:00:00",
  "services": {
    "database": {"status": "healthy"},
    "notifications": {
      "providers": {
        "twilio": {"status": "available"},
        "ultramsg": {"status": "available"},
        "email": {"status": "available"}
      }
    }
  }
}
```

### 2. Test Notification System
```bash
# Test production notifications
python production_notifications.py
```

### 3. Monitor Logs
- **Railway**: Dashboard → Deployments → View Logs
- **Heroku**: `heroku logs --tail`
- **Render**: Dashboard → Logs
- **VPS**: `sudo journalctl -u dealdrip -f`

---

## 🔧 Production Configuration

### Environment Variables Priority
1. **Required**: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` (Primary WhatsApp)
2. **Recommended**: `ULTRAMSG_INSTANCE_ID`, `ULTRAMSG_TOKEN` (Backup WhatsApp)
3. **Fallback**: `EMAIL_USER`, `EMAIL_PASSWORD` (Final fallback)

### Notification Fallback Chain
1. **Twilio WhatsApp** (Free, unlimited, most reliable)
2. **Ultramsg WhatsApp** (Free 1000/month, good reliability)  
3. **Email Notification** (If both WhatsApp methods fail)

### Monitoring URLs
- **Health Check**: `https://your-app.com/api/health`
- **Manual Price Check**: `POST https://your-app.com/api/manual-check`

---

## 🚨 Troubleshooting

### Common Issues

#### 1. "Twilio credentials not found"
- Set `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` environment variables
- Verify credentials in Twilio Console

#### 2. "All notification methods failed"
- Check health endpoint: `/api/health`
- Verify at least one provider shows "available"
- Check environment variables are set correctly

#### 3. Database errors
- For SQLite: ensure write permissions to app directory
- For PostgreSQL: check `DATABASE_URL` format

#### 4. Recipients not receiving WhatsApp
- **Twilio**: Recipients must send `join indicate-iron` to `+1 415 523 8886` first
- **Ultramsg**: Verify WhatsApp Web is connected in Ultramsg dashboard

### Getting Help
1. Check `/api/health` endpoint first
2. Review application logs
3. Test notification system with `production_notifications.py`
4. Verify environment variables are set correctly

---

## 🎉 Success!

Your Dealdrip is now deployed with **enterprise-grade reliability**:
- ✅ **Multiple WhatsApp providers** (never miss a notification)
- ✅ **Email fallback** (guaranteed delivery)
- ✅ **Health monitoring** (track system status)
- ✅ **Free deployment** (no ongoing costs)

**Test it with a product URL and enjoy automated price tracking!** 🛍️

---

## 📋 Quick Commands Reference

### Test Your Deployment
```bash
# Check system health
curl https://your-app.com/api/health

# Test price extraction
curl -X POST https://your-app.com/api/test-price \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.amazon.com/product-url"}'

# Manual price check trigger
curl -X POST https://your-app.com/api/manual-check
```