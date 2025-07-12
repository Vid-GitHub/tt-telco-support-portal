# TT Telco Support Portal - Deployment Guide

## GitHub Setup Instructions

### 1. Create New Repository

```bash
# Navigate to your project directory
cd /path/to/tt-telco-support-portal

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Complete Python web application with chatbot interface"

# Add your GitHub repository as origin
git remote add origin https://github.com/Vid-GitHub/tt-telco-support-portal.git

# Create and switch to main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

### 2. Create Development Branch

```bash
# Create and switch to development branch
git checkout -b development

# Push development branch to GitHub
git push -u origin development
```

## File Checklist for GitHub

Ensure these files are included in your repository:

### Core Application Files
- [x] `app.py` - Main Flask application
- [x] `main.py` - Application entry point
- [x] `requirements.txt` - Python dependencies

### Frontend Files
- [x] `templates/webapp.html` - Main web interface
- [x] `templates/index.html` - API documentation
- [x] `static/style.css` - Application styling
- [x] `static/script.js` - Frontend JavaScript

### Documentation
- [x] `README.md` - Project documentation
- [x] `DEPLOYMENT.md` - This deployment guide
- [x] `replit.md` - Technical architecture documentation
- [x] `.env.example` - Environment variables template

### Configuration
- [x] `.gitignore` - Git ignore rules
- [x] Package configuration files

## Local Development Setup

### Prerequisites
- Python 3.11 or higher
- Git
- Salesforce account with API access

### Setup Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/Vid-GitHub/tt-telco-support-portal.git
   cd tt-telco-support-portal
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Salesforce credentials
   ```

5. **Run Application**
   ```bash
   python main.py
   ```

## Production Deployment

### Using Gunicorn (Recommended)

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
   ```

### Environment Variables for Production

```env
FLASK_ENV=production
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost:5432/tttelco
SALESFORCE_USERNAME=production-username
SALESFORCE_PASSWORD=production-password
SALESFORCE_SECURITY_TOKEN=production-token
```

### Database Migration

For production, consider using PostgreSQL:

```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Set DATABASE_URL in .env
DATABASE_URL=postgresql://username:password@localhost:5432/tttelco
```

## Platform-Specific Deployment

### Heroku
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy to Heroku
heroku create tt-telco-support-portal
heroku config:set SALESFORCE_USERNAME=your-username
heroku config:set SALESFORCE_PASSWORD=your-password
heroku config:set SALESFORCE_SECURITY_TOKEN=your-token
git push heroku main
```

### Railway
```bash
# Create railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main.py",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100
  }
}
```

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "main.py"]
```

## Monitoring and Logging

### Production Logging Setup

```python
import logging
from logging.handlers import RotatingFileHandler

if app.config['ENV'] == 'production':
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

## Security Considerations

1. **Environment Variables**: Never commit `.env` file to Git
2. **HTTPS**: Use HTTPS in production
3. **Database Security**: Use connection pooling and proper credentials
4. **CORS**: Configure CORS for production domains only
5. **Input Validation**: All inputs are validated via Pydantic schemas

## Backup Strategy

1. **Database Backups**: Regular PostgreSQL dumps
2. **Code Backups**: Git repository with multiple branches
3. **Environment Backups**: Secure storage of environment configurations

## Support and Maintenance

- **Logs Location**: `/logs/app.log` in production
- **Health Check**: GET `/` returns 200 if application is healthy
- **API Documentation**: Available at `/api-docs`

For questions or issues, contact the development team or refer to the main README.md file.