# TT Telco Support Portal - Complete Python Web Application

A comprehensive customer service web application built entirely in Python with Flask, featuring an interactive chatbot, account verification, and FAQ management system.

## 🚀 Features

- **Interactive Chatbot Interface**: Guided conversation flow for customer support
- **Account Verification**: Real-time Salesforce integration for customer authentication
- **Task Management**: Automated service request creation and tracking
- **FAQ System**: Searchable knowledge base with rating functionality
- **Modern UI**: Responsive design with TT Telco branding
- **Full Python Stack**: No Node.js or TypeScript dependencies

## 🛠 Technology Stack

- **Backend**: Python 3.11 + Flask
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **Data Storage**: In-memory FAQ storage + Salesforce integration
- **CRM Integration**: Salesforce via simple-salesforce library
- **Styling**: Modern CSS with responsive design
- **Validation**: Pydantic schemas

## 📁 Project Structure

```
/
├── app.py                 # Main Flask application (database-free)
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies (minimal)
├── templates/
│   ├── webapp.html       # Main web application interface
│   └── index.html        # API documentation page
├── static/
│   ├── style.css         # Application styling
│   └── script.js         # Interactive frontend JavaScript
├── README.md             # Project documentation
├── DEPLOYMENT.md         # Deployment instructions
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
└── replit.md            # Technical architecture documentation
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd tt-telco-support-portal
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and configure:

```env
SALESFORCE_USERNAME=your-salesforce-username
SALESFORCE_PASSWORD=your-salesforce-password
SALESFORCE_SECURITY_TOKEN=your-salesforce-security-token
FLASK_ENV=development
PORT=5000
```

### 3. Run the Application

```bash
python main.py
```

Visit `http://localhost:5000` to access the web application.

## 🌐 Application Features

### Chat Support Interface
- Interactive chatbot with guided conversation flow
- Step-by-step account verification process
- Real-time form validation and error handling
- Professional TT Telco branding and messaging

### Account Verification Process
1. Customer enters email address
2. System prompts for full name, date of birth, and issue description
3. Backend verifies account details with Salesforce
4. Creates service task in both Salesforce and local database
5. Provides confirmation with task ID

### FAQ Management
- Search functionality across all FAQ content
- Category-based filtering (Devices, Internet, Mobile Plans, etc.)
- Helpfulness rating system for articles
- Responsive grid layout for optimal viewing

### Error Handling
- Graceful fallback when Salesforce is unavailable
- Clear error messages directing users to support email
- Form validation with user-friendly feedback
- Professional error state messaging

## 🔌 API Endpoints

### Account Verification
```
POST /api/verify-account
Content-Type: application/json

{
  "email": "customer@example.com",
  "fullName": "John Smith",
  "dateOfBirth": "1985-03-15",
  "description": "Need help with NBN connection"
}
```

### FAQ Management
```
GET /api/faq?search=internet&category=Technical
POST /api/faq/:id/rate
```

### Task Retrieval
```
GET /api/tasks
```

## 📱 Responsive Design

The application is fully responsive and works seamlessly across:
- Desktop computers (1200px+)
- Tablets (768px - 1199px)
- Mobile phones (up to 767px)

## 🔒 Security Features

- Input validation using Pydantic schemas
- CORS configuration for secure API access
- Environment variable management for sensitive data
- SQL injection prevention through SQLAlchemy ORM

## 🎨 UI/UX Features

- Modern gradient backgrounds
- TT Telco color scheme and branding
- Smooth animations and transitions
- Loading states and user feedback
- Accessible design patterns

## 📊 Data Storage Architecture

### Salesforce Integration
- **Account Verification**: Real customer data from Salesforce CRM
- **Task Management**: Support tickets created directly in Salesforce
- **Customer Records**: All official data stored in Salesforce

### In-Memory FAQ System
- **Knowledge Base**: FAQ articles stored in application memory
- **Search & Filter**: Fast local search without database queries
- **Rating System**: Helpfulness tracking for content improvement

## 🚀 Deployment

### Development
```bash
python main.py
```

### Production
1. Set `FLASK_ENV=production`
2. Configure Salesforce credentials
3. Use production WSGI server (gunicorn)
4. Set up proper logging and monitoring

### Environment Variables
- `SALESFORCE_USERNAME`: Salesforce login email
- `SALESFORCE_PASSWORD`: Salesforce password
- `SALESFORCE_SECURITY_TOKEN`: Salesforce security token

- `FLASK_ENV`: Environment mode (development/production)
- `PORT`: Server port (default: 5000)

## 🤝 Support

For technical issues or questions:
- **Email**: support@yopmail.com
- **Documentation**: Visit `/api-docs` for API documentation

## 📝 License

This project is proprietary software for TT Telco customer service operations.

---

**TT Telco Support Portal v1.0.0** - Complete Python Web Application