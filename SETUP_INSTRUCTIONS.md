# CRM LaitusNeo Setup Instructions

## Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- XAMPP (for MySQL database)
- Git

## Backend Setup

### 1. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Database Setup
1. Start XAMPP and ensure MySQL is running
2. Open phpMyAdmin (http://localhost/phpmyadmin)
3. Create a new database named `crm_laitusneo`
4. Run the database setup script:
   ```bash
   python database_setup.py
   ```

### 3. Configure Environment Variables
Create a `.env` file in the backend directory:
```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=crm_laitusneo

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### 4. Start the Backend Server
```bash
python run.py
```
The backend will be available at `http://localhost:5000`

## Frontend Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Start the Development Server
```bash
npm start
```
The frontend will be available at `http://localhost:3000`

## Testing the Application

### 1. Access the Application
- Open your browser and go to `http://localhost:3000`
- You should be redirected to the login page

### 2. Test with Default Admin User
- Email: `admin@crm.com`
- Password: `Admin123!`
- User Type: Main User

### 3. Create a New User
- Click "Sign up here" on the login page
- Fill in the signup form
- Only Main Users can sign up

### 4. Test Different User Types
- Use the dropdown to switch between Main User and Sub User
- Note: Sub users cannot sign up, they must be created by main users

## API Testing with Postman

### 1. Import the Collection
- Open Postman
- Import the API collection from `API_DOCUMENTATION.md`
- Follow the setup instructions in the documentation

### 2. Test Endpoints
1. Health Check: `GET /api/health`
2. Signup: `POST /api/auth/signup`
3. Login: `POST /api/auth/login`
4. Get Current User: `GET /api/auth/me`
5. Verify Token: `POST /api/auth/verify-token`

## Troubleshooting

### Common Issues

#### Backend Issues
1. **Database Connection Error**
   - Ensure XAMPP MySQL is running
   - Check database credentials in `.env` file
   - Verify database `crm_laitusneo` exists

2. **Port Already in Use**
   - Change the port in `run.py` from 5000 to another port
   - Update the frontend API base URL accordingly

3. **Module Not Found**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python virtual environment is activated

#### Frontend Issues
1. **API Connection Error**
   - Ensure backend server is running on port 5000
   - Check CORS settings in backend
   - Verify API base URL in `AuthContext.js`

2. **Build Errors**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check for syntax errors in React components

#### Database Issues
1. **Tables Not Created**
   - Run `python database_setup.py` again
   - Check database permissions
   - Verify database connection

2. **Default User Not Created**
   - Manually create admin user in database
   - Or run the setup script again

## Security Notes

### Production Deployment
1. Change the JWT secret key in production
2. Use environment variables for all sensitive data
3. Enable HTTPS
4. Set up proper CORS policies
5. Use a production database (not XAMPP)
6. Implement rate limiting
7. Add input validation and sanitization

### Password Security
- Passwords are hashed using bcrypt
- Minimum password requirements are enforced
- JWT tokens expire after 1 hour

## File Structure
```
CRM/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── models.py              # Database models
│   ├── config.py              # Configuration settings
│   ├── run.py                 # Application runner
│   ├── database_setup.py      # Database setup script
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── src/
│   ├── components/
│   │   ├── Auth/              # Authentication components
│   │   │   ├── Login.js
│   │   │   ├── Signup.js
│   │   │   ├── ProtectedRoute.js
│   │   │   └── Auth.css
│   │   └── Navigation/        # Navigation component
│   ├── contexts/
│   │   └── AuthContext.js     # Authentication context
│   └── Assets/
│       └── logo.png           # Application logo
├── API_DOCUMENTATION.md       # API documentation
└── SETUP_INSTRUCTIONS.md      # This file
```

## Support
If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure all services are running
4. Check the console for error messages
5. Review the API documentation for endpoint details
