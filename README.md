# 🚀 CRM LaitusNeo - Customer Relationship Management System

[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.2.5-green.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive, full-stack Customer Relationship Management (CRM) system built with React and Flask. Features dual user interfaces for main users and salesmen, complete with lead management, deal tracking, product management, and comprehensive reporting capabilities.

## ✨ Features

### 🎯 Core Functionality
- **Dual User System**: Separate interfaces for main users and salesmen
- **Lead Management**: Complete lead lifecycle from creation to conversion
- **Deal Pipeline**: Track deals from initial contact to closure
- **Product Management**: Comprehensive product catalog with pricing
- **Salesman Management**: Create, manage, and track salesman performance
- **Task Assignment**: Assign products and targets to salesmen
- **Report Generation**: Detailed reports with PDF export functionality

### 🔐 Authentication & Security
- **JWT Authentication**: Secure token-based authentication
- **Role-based Access**: Different permissions for main users and salesmen
- **Password Security**: Bcrypt hashing with validation requirements
- **Protected Routes**: Secure access to different application sections

### 📊 Dashboard & Analytics
- **Interactive Charts**: Sales performance visualization with Recharts
- **Metrics Cards**: Key performance indicators at a glance
- **Real-time Updates**: Live data updates across the application
- **Responsive Design**: Mobile-friendly interface

### 🛠️ Technical Features
- **RESTful API**: Well-documented Flask REST API with Swagger UI
- **Database Integration**: MySQL with SQLAlchemy ORM
- **Modern UI**: Clean, professional interface with smooth animations
- **Export Functionality**: PDF report generation
- **API Documentation**: Interactive Swagger documentation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  Flask Backend  │    │   MySQL Database│
│                 │    │                 │    │                 │
│ • Main User UI  │◄──►│ • REST API      │◄──►│ • User Data     │
│ • Salesman UI   │    │ • JWT Auth      │    │ • Leads/Deals   │
│ • Dashboard     │    │ • Swagger Docs  │    │ • Products      │
│ • Reports       │    │ • CORS Enabled  │    │ • Tasks         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **MySQL 8.0+** (or XAMPP)
- **Git**

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/crm-laitusneo.git
cd crm-laitusneo
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Database Configuration
1. Start MySQL (or XAMPP)
2. Create database: `crm_laitusneo`
3. Create `.env` file in backend directory:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=crm_laitusneo
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_ACCESS_TOKEN_EXPIRES=3600
FLASK_ENV=development
FLASK_DEBUG=True
```

#### Initialize Database
```bash
python database_setup.py
```

#### Start Backend Server
```bash
python run.py
```
Backend will be available at `http://localhost:5000`

### 3. Frontend Setup

#### Install Dependencies
```bash
npm install
```

#### Start Development Server
```bash
npm start
```
Frontend will be available at `http://localhost:3000`

## 📱 User Interfaces

### Main User Dashboard
- **Overview**: Sales metrics and performance charts
- **Salesman Management**: Create and manage sales team
- **Lead Management**: View all leads from salesmen
- **Product Management**: Manage product catalog
- **Reports**: Generate and export detailed reports

### Salesman Portal
- **Task Management**: View assigned products and targets
- **Lead Management**: Create and manage leads
- **Deal Pipeline**: Track deals and update status
- **Meeting Management**: Schedule and track meetings
- **Pitch Deck**: Access presentation materials

## 🔧 API Documentation

### Interactive Documentation
- **Swagger UI**: `http://localhost:5000/api/docs/`
- **API Root**: `http://localhost:5000/`
- **Health Check**: `http://localhost:5000/api/health`

### Key Endpoints
```bash
# Authentication
POST /api/auth/signup          # User registration
POST /api/auth/login           # User login
GET  /api/auth/me             # Get current user

# Lead Management
GET    /api/leads             # List leads
POST   /api/leads             # Create lead
PUT    /api/leads/{id}        # Update lead
PATCH  /api/leads/{id}/status # Update lead status

# Deal Management
GET    /api/deals             # List deals
POST   /api/deals             # Create deal
PATCH  /api/deals/{id}/status # Update deal status

# Salesman Management
GET    /api/salesmen          # List salesmen
POST   /api/salesmen          # Create salesman
PUT    /api/salesmen/{id}     # Update salesman
```

## 🧪 Testing

### Default Test Credentials
- **Main User**: `admin@crm.com` / `Admin123!`
- **Salesman**: Created through main user interface

### API Testing
Use the Swagger UI at `http://localhost:5000/api/docs/` for interactive API testing.

## 📁 Project Structure

```
crm-laitusneo/
├── backend/                    # Flask Backend
│   ├── app.py                 # Main Flask application
│   ├── models.py              # Database models
│   ├── config.py              # Configuration
│   ├── database_setup.py      # Database initialization
│   ├── run.py                 # Application runner
│   ├── requirements.txt       # Python dependencies
│   └── swagger/               # API documentation
├── src/                       # React Frontend
│   ├── components/            # React components
│   │   ├── Auth/             # Authentication components
│   │   ├── Dashboard/        # Main dashboard
│   │   ├── LeadManagement/   # Lead management
│   │   ├── SalesmanManagement/ # Salesman management
│   │   ├── ProductManagement/ # Product management
│   │   └── SubUser/          # Salesman interface
│   ├── contexts/             # React contexts
│   ├── services/             # API services
│   └── Assets/               # Static assets
├── public/                   # Public assets
├── package.json              # Node.js dependencies
└── README.md                 # This file
```

## 🛠️ Technology Stack

### Frontend
- **React 18.2.0** - Modern React with hooks
- **React Router 6.3.0** - Client-side routing
- **Recharts 2.5.0** - Data visualization
- **Lucide React** - Modern icon library
- **Axios 1.5.0** - HTTP client
- **jsPDF** - PDF generation

### Backend
- **Flask 2.2.5** - Python web framework
- **Flask-RESTX 1.1.0** - REST API framework
- **SQLAlchemy 1.4.53** - Database ORM
- **Flask-JWT-Extended 4.5.3** - JWT authentication
- **PyMySQL 1.1.0** - MySQL connector
- **bcrypt 4.0.1** - Password hashing

### Database
- **MySQL 8.0** - Primary database
- **SQLAlchemy ORM** - Database abstraction

## 🚀 Deployment

### Production Considerations
1. **Environment Variables**: Set production environment variables
2. **Database**: Use production MySQL instance
3. **Security**: Change JWT secret key
4. **HTTPS**: Enable SSL/TLS
5. **CORS**: Configure for production domains
6. **Rate Limiting**: Implement API rate limiting

### Build for Production
```bash
# Frontend
npm run build

# Backend
# Ensure production environment variables are set
python run.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the [Setup Instructions](SETUP_INSTRUCTIONS.md)
- **Issues**: Create an issue in the GitHub repository
- **API Docs**: Visit `http://localhost:5000/api/docs/` when running

## 🎯 Roadmap

- [ ] Real-time notifications with WebSocket
- [ ] Advanced analytics and reporting
- [ ] Mobile application
- [ ] Email integration
- [ ] Calendar integration
- [ ] Advanced search and filtering
- [ ] Data import/export
- [ ] Multi-language support

---

**Made with ❤️ for modern CRM needs**