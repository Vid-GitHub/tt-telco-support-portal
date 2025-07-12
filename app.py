#!/usr/bin/env python3
"""
TT Telco Support Portal - Python Flask Backend (No Database)
A customer service application with Salesforce integration only
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from werkzeug.exceptions import BadRequest
from pydantic import BaseModel, EmailStr, Field, ValidationError
import os
from datetime import datetime
import logging
from typing import Optional, List, Dict, Any
from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configure CORS
CORS(app, origins=['*'])

# Basic app configuration

# In-memory FAQ storage (no database needed)
FAQ_ARTICLES = [
    {
        "id": 1,
        "title": "How to troubleshoot NBN connection issues",
        "content": "1. Check all cables are connected properly. 2. Restart your modem by unplugging for 30 seconds. 3. Check for service outages in your area. 4. Contact support if issues persist.",
        "category": "Technical Support",
        "views": 0,
        "helpful": 0,
        "notHelpful": 0
    },
    {
        "id": 2,
        "title": "How to change your mobile plan",
        "content": "1. Log into your TT Telco account online. 2. Go to 'My Plans' section. 3. Select 'Change Plan' option. 4. Choose your new plan and confirm changes. Changes take effect from next billing cycle.",
        "category": "Mobile Plans",
        "views": 0,
        "helpful": 0,
        "notHelpful": 0
    },
    {
        "id": 3,
        "title": "Understanding your mobile data usage",
        "content": "Monitor your data usage through: 1. TT Telco mobile app. 2. Online account portal. 3. SMS alerts when reaching 80% usage. 4. Phone settings data usage tracker.",
        "category": "Mobile Plans",
        "views": 0,
        "helpful": 0,
        "notHelpful": 0
    },
    {
        "id": 4,
        "title": "How to update your account details",
        "content": "1. Log into your online account. 2. Navigate to 'Account Settings'. 3. Update your personal information. 4. Verify changes via email or SMS. 5. Save changes to complete the update.",
        "category": "Account Management",
        "views": 0,
        "helpful": 0,
        "notHelpful": 0
    },
    {
        "id": 5,
        "title": "Setting up Wi-Fi on your device",
        "content": "1. Find your Wi-Fi network name and password (usually on modem label). 2. Go to device Wi-Fi settings. 3. Select your network. 4. Enter password. 5. Connect and test internet access.",
        "category": "Devices",
        "views": 0,
        "helpful": 0,
        "notHelpful": 0
    },
    {
        "id": 6,
        "title": "Can I bring my own phone (BYO)?",
        "content": "Yes, you can bring your own compatible device to TT Telco. Your device needs to be unlocked and compatible with our network. You can check device compatibility on our website or contact our support team.",
        "category": "Devices",
        "views": 0,
        "helpful": 0,
        "notHelpful": 0
    },
    {
        "id": 7,
        "title": "How do I set up my new NBN connection?",
        "content": "Setting up your NBN connection: 1) Connect your modem to the NBN connection box, 2) Power on your modem and wait for all lights to turn green, 3) Connect your devices via WiFi or ethernet cable, 4) Test your connection. If you need help, our technical support team is available 24/7.",
        "category": "Internet",
        "views": 0,
        "helpful": 0,
        "notHelpful": 0
    },
    {
        "id": 8,
        "title": "What are TT Telco's mobile plan options?",
        "content": "TT Telco offers flexible mobile plans: Basic Plan (10GB data, unlimited calls/SMS), Standard Plan (25GB data, unlimited calls/SMS), Premium Plan (50GB data, unlimited calls/SMS, international calls included). All plans include 5G access where available.",
        "category": "Mobile Plans",
        "views": 0,
        "helpful": 0,
        "notHelpful": 0
    }
]

# Pydantic Schemas
class VerifyAccount(BaseModel):
    email: EmailStr
    fullName: str = Field(..., min_length=1, max_length=255)
    dateOfBirth: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)

class FaqRating(BaseModel):
    helpful: bool

# Salesforce Service
class SalesforceService:
    def __init__(self):
        self.sf = None
        self.credentials_available = self._check_credentials()
        if self.credentials_available:
            try:
                self._connect()
            except Exception as e:
                logger.warning(f"Salesforce connection failed during startup: {str(e)}")
                self.sf = None
    
    def _check_credentials(self):
        username = os.getenv('SALESFORCE_USERNAME')
        password = os.getenv('SALESFORCE_PASSWORD')
        return bool(username and password)
    
    def _connect(self):
        try:
            username = os.getenv('SALESFORCE_USERNAME')
            password = os.getenv('SALESFORCE_PASSWORD')
            security_token = os.getenv('SALESFORCE_SECURITY_TOKEN', '')
            
            if not username or not password:
                logger.error("Salesforce credentials not configured")
                raise ValueError("Salesforce credentials not configured")
            
            self.sf = Salesforce(
                username=username,
                password=password,
                security_token=security_token,
                domain='login',
                version='60.0'
            )
            logger.info("Successfully connected to Salesforce")
            
        except Exception as e:
            logger.error(f"Failed to connect to Salesforce: {str(e)}")
            self.sf = None
            raise
    
    def _ensure_connection(self):
        if not self.sf:
            self._connect()
    
    def verify_account(self, email: str, full_name: str, date_of_birth: str) -> Optional[Dict[str, Any]]:
        try:
            self._ensure_connection()
            
            query = f"""
                SELECT Id, Name, Email__c, Date_Of_Birth__c 
                FROM Account 
                WHERE Email__c = '{email}' 
                AND Name = '{full_name}'
                AND Date_Of_Birth__c = {date_of_birth}
                LIMIT 1
            """
            
            result = self.sf.query(query)
            
            if result['totalSize'] > 0:
                return result['records'][0]
            return None
                
        except Exception as e:
            logger.error(f"Account verification failed: {str(e)}")
            raise Exception(f"Failed to verify account with Salesforce: {str(e)}")
    
    def create_task(self, account_id: str, description: str) -> Dict[str, Any]:
        try:
            self._ensure_connection()
            
            task_data = {
                'Subject': 'Customer Service Request',
                'Description': description,
                'WhatId': account_id,
                'Status': 'Not Started',
                'Priority': 'Normal'
            }
            
            result = self.sf.Task.create(task_data)
            
            if result['success']:
                return {
                    'Id': result['id'],
                    'Subject': task_data['Subject'],
                    'Description': task_data['Description'],
                    'WhatId': account_id,
                    'Status': task_data['Status']
                }
            else:
                raise Exception(f"Failed to create task: {result}")
                
        except Exception as e:
            logger.error(f"Task creation failed: {str(e)}")
            raise Exception(f"Failed to create task in Salesforce: {str(e)}")

# Initialize services
salesforce_service = SalesforceService()

# Error handlers
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Unhandled error: {str(error)}")
    return jsonify({
        'message': 'An internal error occurred',
        'error': str(error) if app.debug else 'Internal server error'
    }), 500

@app.errorhandler(BadRequest)
def handle_bad_request(error):
    return jsonify({
        'message': 'Invalid request data',
        'error': str(error.description)
    }), 400

# API Routes
@app.route('/api/verify-account', methods=['POST'])
def verify_account():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        # Validate input
        try:
            verify_data = VerifyAccount(**data)
        except ValidationError as e:
            return jsonify({'message': f'Validation error: {str(e)}'}), 400
        
        # Verify account with Salesforce
        salesforce_account = salesforce_service.verify_account(
            verify_data.email,
            verify_data.fullName,
            verify_data.dateOfBirth
        )
        
        if not salesforce_account:
            return jsonify({
                'verified': False,
                'message': 'Account not found or details do not match our records. Please check your information or contact support at support@yopmail.com.'
            }), 404
        
        # Create task in Salesforce
        salesforce_task = salesforce_service.create_task(
            salesforce_account['Id'],
            verify_data.description
        )
        
        return jsonify({
            'verified': True,
            'message': 'Account verified successfully! Your support request has been created.',
            'taskId': salesforce_task['Id'],
            'accountId': salesforce_account['Id'],
            'details': {
                'name': salesforce_account['Name'],
                'email': salesforce_account.get('Email__c', verify_data.email),
                'taskSubject': salesforce_task['Subject'],
                'taskStatus': salesforce_task['Status']
            }
        })
        
    except Exception as e:
        logger.error(f"Account verification error: {str(e)}")
        return jsonify({
            'verified': False,
            'message': 'We are currently experiencing technical difficulties. Please contact support at support@yopmail.com or try again later.'
        }), 500

@app.route('/api/faq', methods=['GET'])
def get_faqs():
    try:
        search = request.args.get('search', '').lower()
        category = request.args.get('category', '')
        
        # Filter FAQ articles from in-memory storage
        filtered_faqs = FAQ_ARTICLES.copy()
        
        if search:
            filtered_faqs = [
                faq for faq in filtered_faqs 
                if search in faq['title'].lower() or search in faq['content'].lower()
            ]
        
        if category and category != 'all':
            filtered_faqs = [
                faq for faq in filtered_faqs 
                if faq['category'] == category
            ]
        
        return jsonify(filtered_faqs)
        
    except Exception as e:
        logger.error(f"FAQ fetch error: {str(e)}")
        return jsonify({'message': 'Failed to fetch FAQs'}), 500

@app.route('/api/faq/<int:faq_id>/rate', methods=['POST'])
def rate_faq(faq_id: int):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        # Validate input
        try:
            rating_data = FaqRating(**data)
        except ValidationError as e:
            return jsonify({'message': f'Validation error: {str(e)}'}), 400
        
        # Find FAQ article in memory
        faq_article = None
        for faq in FAQ_ARTICLES:
            if faq['id'] == faq_id:
                faq_article = faq
                break
        
        if not faq_article:
            return jsonify({'message': 'FAQ article not found'}), 404
        
        # Update rating
        if rating_data.helpful:
            faq_article['helpful'] += 1
        else:
            faq_article['notHelpful'] += 1
        
        return jsonify({
            'message': 'Thank you for your feedback!',
            'helpful': faq_article['helpful'],
            'notHelpful': faq_article['notHelpful']
        })
        
    except Exception as e:
        logger.error(f"FAQ rating error: {str(e)}")
        return jsonify({'message': 'Failed to submit rating'}), 500

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get tasks from Salesforce only"""
    try:
        # For this simple version, we'll return a message that tasks are managed in Salesforce
        return jsonify({
            'message': 'Tasks are managed in Salesforce CRM system',
            'salesforce_access': salesforce_service.credentials_available
        })
        
    except Exception as e:
        logger.error(f"Tasks fetch error: {str(e)}")
        return jsonify({'message': 'Failed to fetch tasks'}), 500

@app.route('/')
def serve_frontend():
    try:
        return render_template('webapp.html')
    except Exception as e:
        logger.error(f"Failed to serve frontend: {str(e)}")
        return render_template('index.html')

@app.route('/api-docs')
def api_documentation():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"🚀 Starting TT Telco Support Portal on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)