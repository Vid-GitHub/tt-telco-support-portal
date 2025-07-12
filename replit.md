# TT Telco Support Portal - Python Flask Backend

## Overview

TT Telco Support Portal is a modern customer service application built with **Python Flask**. The application provides an automated customer service portal specifically designed for TT Telco customers, featuring account verification, task creation, comprehensive FAQ management with TT Telco content, and REST API endpoints for frontend integration. It integrates with Salesforce for CRM functionality and uses SQLite/PostgreSQL for data persistence.

## Recent Changes (July 12, 2025)

- ✅ Completely converted application from TypeScript/Node.js to Python Flask
- ✅ Removed all TypeScript, React, and Node.js dependencies and code
- ✅ Created Flask backend with SQLAlchemy ORM for database operations
- ✅ Integrated simple-salesforce library for Salesforce CRM connectivity
- ✅ Added Pydantic validation for API request/response schemas
- ✅ Built complete web interface with interactive chatbot and modern UI
- ✅ Created comprehensive FAQ system with search, filtering, and rating
- ✅ Implemented responsive design with professional TT Telco branding
- ✅ Prepared complete codebase for GitHub deployment with documentation
- ✅ Application fully tested and running with Salesforce integration working
- ✅ Removed local database dependency - now uses Salesforce + in-memory FAQ storage
- ✅ Simplified architecture with fewer dependencies and faster performance
- ✅ Cleaned up codebase - removed all unwanted files, old database code, and unused dependencies
- ✅ Optimized project structure for production deployment

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Python Project Structure
The application follows a clean Python Flask structure:
- `app.py` - Main Flask application with routes and models
- `main.py` - Application entry point
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates for API documentation
- `README.md` - Comprehensive documentation

### Technology Stack
- **Backend**: Python Flask web framework
- **Database**: SQLAlchemy ORM with SQLite (PostgreSQL ready)
- **External Integration**: Salesforce via simple-salesforce library
- **Data Validation**: Pydantic for request/response schemas
- **API**: RESTful endpoints with JSON responses
- **Configuration**: Environment variables for deployment settings

## Key Components

### Frontend Architecture
- **Component Structure**: Uses shadcn/ui design system with Radix UI primitives
- **State Management**: TanStack Query for API state, React hooks for local state
- **Styling Strategy**: Tailwind CSS with custom CSS variables for consistent theming
- **Form Validation**: Zod schemas shared between frontend and backend
- **Responsive Design**: Mobile-first approach with responsive breakpoints

### Backend Architecture
- **API Design**: RESTful endpoints with Express.js
- **Data Layer**: Drizzle ORM with PostgreSQL for type-safe database operations
- **Validation**: Zod schemas for request/response validation
- **File Handling**: Multer for file uploads (FAQ documents)
- **External Services**: Salesforce integration for account verification and task management

### Database Schema
- **Users**: Basic user authentication (prepared but not implemented)
- **Accounts**: Customer account information with Salesforce integration
- **Tasks**: Service requests linked to accounts and Salesforce tasks
- **FAQ Articles**: Knowledge base content with rating system

### Core Features
1. **Interactive Chatbot**: Guided conversation flow for account verification and task creation
2. **Account Verification**: Integration with Salesforce to verify customer details
3. **Task Management**: Creation and tracking of service requests
4. **FAQ System**: Searchable knowledge base with file upload capability
5. **Responsive UI**: Modern interface that works across all device sizes

## Data Flow

### Account Verification Flow
1. User provides email through chatbot interface
2. User completes verification form with full name, date of birth, and issue description
3. Backend queries Salesforce to verify account details
4. If verified, creates task in both Salesforce and local database
5. Returns success confirmation with task ID

### FAQ Management Flow
1. Users can search and filter FAQ articles by category
2. Admin can upload FAQ documents (txt, doc, docx, pdf)
3. Articles support view tracking and helpfulness ratings
4. Search functionality across title and content

### File Upload Flow
1. Frontend validates file types (txt, doc, docx, pdf)
2. Multer middleware processes uploaded files
3. Backend extracts content and creates FAQ articles
4. Success/error feedback provided to user

## External Dependencies

### Salesforce Integration
- **Authentication**: Username/password with security token
- **Account Verification**: Query accounts by email, name, and date of birth
- **Task Creation**: Create service tasks linked to verified accounts
- **Error Handling**: Graceful fallback when Salesforce is unavailable

### Database Dependencies
- **Neon Database**: Serverless PostgreSQL hosting
- **Connection Management**: Environment-based connection strings
- **Migration Support**: Drizzle Kit for schema migrations

### UI Dependencies
- **Radix UI**: Accessible component primitives
- **Lucide Icons**: Consistent iconography
- **Tailwind CSS**: Utility-first styling
- **shadcn/ui**: Pre-built component library

## Deployment Strategy

### Development Environment
- **Vite Dev Server**: Hot module replacement for frontend development
- **Express Server**: Development server with logging and error handling
- **Environment Variables**: Database URL and Salesforce credentials

### Production Build
- **Frontend**: Vite builds optimized static assets to `dist/public`
- **Backend**: esbuild bundles server code to `dist/index.js`
- **Static Serving**: Express serves built frontend in production
- **Process Management**: Single Node.js process serves both frontend and API

### Database Management
- **Schema Migrations**: Drizzle Kit for database schema updates
- **Connection Pooling**: Neon serverless handles connection management
- **Environment Configuration**: DATABASE_URL for connection string

### Error Handling
- **Frontend**: Global error boundaries and toast notifications
- **Backend**: Centralized error middleware with status codes
- **Logging**: Request/response logging for API endpoints
- **Graceful Degradation**: Fallbacks when external services are unavailable

The application is designed to be deployed on platforms like Replit, with configuration optimized for single-process deployment and serverless database hosting.