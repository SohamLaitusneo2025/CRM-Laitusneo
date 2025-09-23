"""
Swagger API Documentation Setup
"""

from flask_restx import Api, Namespace, Resource, fields
from flask import Blueprint
from .config import SWAGGER_CONFIG

# Create Blueprint for Swagger
swagger_bp = Blueprint('swagger', __name__, url_prefix='/api/docs')

# Initialize API with Swagger configuration
api = Api(
    swagger_bp,
    title=SWAGGER_CONFIG['title'],
    version=SWAGGER_CONFIG['version'],
    description=SWAGGER_CONFIG['description'],
    contact=SWAGGER_CONFIG['contact'],
    license=SWAGGER_CONFIG['license'],
    doc='/',  # Swagger UI will be available at /api/docs/
    security='Bearer'
)

# Define schemas directly in the API
user_model = api.model('User', {
    'id': fields.Integer(required=True, description='User ID'),
    'email': fields.String(required=True, description='User email address'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'is_active': fields.Boolean(required=True, description='User active status'),
    'created_at': fields.DateTime(required=True, description='User creation timestamp'),
    'updated_at': fields.DateTime(required=True, description='User last update timestamp')
})

registration_model = api.model('Registration', {
    'email': fields.String(required=True, description='User email address', example='user@example.com'),
    'password': fields.String(required=True, description='User password (min 6 characters)', example='password123'),
    'firstName': fields.String(required=True, description='User first name', example='John'),
    'lastName': fields.String(required=True, description='User last name', example='Doe')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email address', example='user@example.com'),
    'password': fields.String(required=True, description='User password', example='password123'),
    'userType': fields.String(required=False, description='User type (optional)', example='admin')
})

success_response_model = api.model('SuccessResponse', {
    'message': fields.String(required=True, description='Success message'),
    'user': fields.Nested(user_model, required=False, description='User information')
})

error_response_model = api.model('ErrorResponse', {
    'error': fields.String(required=True, description='Error message'),
    'details': fields.String(required=False, description='Additional error details')
})

token_verification_model = api.model('TokenVerification', {
    'valid': fields.Boolean(required=True, description='Token validity status'),
    'user': fields.Nested(user_model, required=False, description='User information')
})

api_info_model = api.model('APIInfo', {
    'message': fields.String(required=True, description='API welcome message'),
    'version': fields.String(required=True, description='API version'),
    'endpoints': fields.Raw(required=True, description='Available API endpoints'),
    'status': fields.String(required=True, description='API status')
})

health_model = api.model('Health', {
    'status': fields.String(required=True, description='API health status'),
    'timestamp': fields.DateTime(required=True, description='Health check timestamp'),
    'version': fields.String(required=True, description='API version'),
    'database': fields.String(required=True, description='Database connection status')
})

# Create namespaces
auth_ns = Namespace('Authentication', description='User authentication and authorization endpoints')
health_ns = Namespace('Health', description='API health check endpoints')
root_ns = Namespace('Root', description='API information and root endpoints')

# Add namespaces to API
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(health_ns, path='/health')
api.add_namespace(root_ns, path='/')

# Registration endpoint documentation
@auth_ns.route('/signup')
class UserRegistration(Resource):
    @auth_ns.expect(registration_model, validate=True)
    @auth_ns.response(201, 'User created successfully', success_response_model)
    @auth_ns.response(400, 'Bad request', error_response_model)
    @auth_ns.response(409, 'User already exists', error_response_model)
    @auth_ns.response(500, 'Internal server error', error_response_model)
    def post(self):
        """
        Register a new user
        
        Creates a new user account with the provided information.
        The password will be securely hashed before storage.
        
        **Example Request:**
        ```json
        {
            "email": "user@example.com",
            "password": "password123",
            "firstName": "John",
            "lastName": "Doe"
        }
        ```
        
        **Example Response:**
        ```json
        {
            "message": "User created successfully",
            "user": {
                "id": 1,
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "is_active": true,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }
        ```
        """
        pass

# Login endpoint documentation
@auth_ns.route('/login')
class UserLogin(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.response(200, 'Login successful', success_response_model)
    @auth_ns.response(401, 'Invalid credentials', error_response_model)
    @auth_ns.response(400, 'Bad request', error_response_model)
    @auth_ns.response(500, 'Internal server error', error_response_model)
    def post(self):
        """
        User login
        
        Authenticates a user with email and password.
        Returns a JWT token for subsequent API requests.
        
        **Example Request:**
        ```json
        {
            "email": "user@example.com",
            "password": "password123",
            "userType": "admin"
        }
        ```
        
        **Example Response:**
        ```json
        {
            "message": "Login successful",
            "user": {
                "id": 1,
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "is_active": true,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }
        ```
        """
        pass

# Token verification endpoint documentation
@auth_ns.route('/verify-token')
class TokenVerification(Resource):
    @auth_ns.response(200, 'Token is valid', token_verification_model)
    @auth_ns.response(401, 'Invalid or expired token', error_response_model)
    @auth_ns.response(500, 'Internal server error', error_response_model)
    def get(self):
        """
        Verify JWT token
        
        Validates the provided JWT token and returns user information if valid.
        This endpoint requires a valid JWT token in the Authorization header.
        
        **Headers:**
        ```
        Authorization: Bearer <your_jwt_token>
        ```
        
        **Example Response:**
        ```json
        {
            "valid": true,
            "user": {
                "id": 1,
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "is_active": true,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }
        ```
        """
        pass

# User profile endpoint documentation
@auth_ns.route('/me')
class UserProfile(Resource):
    @auth_ns.response(200, 'User profile retrieved', user_model)
    @auth_ns.response(401, 'Unauthorized', error_response_model)
    @auth_ns.response(500, 'Internal server error', error_response_model)
    def get(self):
        """
        Get current user profile
        
        Returns the profile information of the currently authenticated user.
        This endpoint requires a valid JWT token in the Authorization header.
        
        **Headers:**
        ```
        Authorization: Bearer <your_jwt_token>
        ```
        
        **Example Response:**
        ```json
        {
            "id": 1,
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "is_active": true,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        ```
        """
        pass

# Health check endpoint documentation
@health_ns.route('/')
class HealthCheck(Resource):
    @health_ns.response(200, 'API is healthy', health_model)
    def get(self):
        """
        API Health Check
        
        Returns the current health status of the API and its dependencies.
        
        **Example Response:**
        ```json
        {
            "status": "healthy",
            "timestamp": "2024-01-01T00:00:00Z",
            "version": "1.0.0",
            "database": "connected"
        }
        ```
        """
        pass

# Root endpoint documentation
@root_ns.route('/')
class RootInfo(Resource):
    @root_ns.response(200, 'API information', api_info_model)
    def get(self):
        """
        API Root Information
        
        Returns basic information about the API including available endpoints.
        
        **Example Response:**
        ```json
        {
            "message": "CRM LaitusNeo API Server",
            "version": "1.0.0",
            "endpoints": {
                "health": "GET /api/health",
                "signup": "POST /api/auth/signup",
                "login": "POST /api/auth/login",
                "me": "GET /api/auth/me",
                "verify_token": "GET /api/auth/verify-token"
            },
            "status": "running"
        }
        ```
        """
        pass
