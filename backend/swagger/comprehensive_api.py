"""
Comprehensive Swagger API Documentation for CRM LaitusNeo
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

# ==================== DATA MODELS ====================

# User Models
user_model = api.model('User', {
    'id': fields.Integer(required=True, description='User ID'),
    'email': fields.String(required=True, description='User email address'),
    'username': fields.String(required=False, description='Username for sub-users'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'user_type': fields.String(required=True, description='User type (main/sub)'),
    'is_active': fields.Boolean(required=True, description='User active status'),
    'contact_number': fields.String(required=False, description='Contact number'),
    'main_user_id': fields.Integer(required=False, description='Main user ID for sub-users'),
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
    'email': fields.String(required=False, description='User email address', example='user@example.com'),
    'username': fields.String(required=False, description='Username for sub-users', example='SM1234'),
    'password': fields.String(required=True, description='User password', example='password123'),
    'userType': fields.String(required=True, description='User type (main/sub)', example='main')
})

# Salesman Models
salesman_create_model = api.model('SalesmanCreate', {
    'name': fields.String(required=True, description='Full name of the salesman', example='John Doe'),
    'contactNumber': fields.String(required=True, description='Contact number', example='+1234567890'),
    'email': fields.String(required=True, description='Email address', example='john@example.com')
})

salesman_update_model = api.model('SalesmanUpdate', {
    'first_name': fields.String(required=False, description='First name'),
    'last_name': fields.String(required=False, description='Last name'),
    'email': fields.String(required=False, description='Email address'),
    'contact_number': fields.String(required=False, description='Contact number'),
    'is_active': fields.Boolean(required=False, description='Active status')
})

salesman_credentials_model = api.model('SalesmanCredentials', {
    'username': fields.String(required=True, description='Generated username'),
    'password': fields.String(required=True, description='Generated password')
})

salesman_response_model = api.model('SalesmanResponse', {
    'message': fields.String(required=True, description='Response message'),
    'user': fields.Nested(user_model, required=True, description='Salesman information'),
    'credentials': fields.Nested(salesman_credentials_model, required=False, description='Login credentials')
})

# Product Models
product_model = api.model('Product', {
    'id': fields.Integer(required=True, description='Product ID'),
    'name': fields.String(required=True, description='Product name'),
    'description': fields.String(required=False, description='Product description'),
    'price': fields.Float(required=True, description='Product price'),
    'category': fields.String(required=False, description='Product category'),
    'is_active': fields.Boolean(required=True, description='Product active status'),
    'created_at': fields.DateTime(required=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(required=True, description='Last update timestamp')
})

product_create_model = api.model('ProductCreate', {
    'name': fields.String(required=True, description='Product name', example='E-School Software'),
    'description': fields.String(required=False, description='Product description', example='Educational management system'),
    'price': fields.Float(required=True, description='Product price', example=10000.0),
    'category': fields.String(required=False, description='Product category', example='Software')
})

product_update_model = api.model('ProductUpdate', {
    'name': fields.String(required=False, description='Product name'),
    'description': fields.String(required=False, description='Product description'),
    'price': fields.Float(required=False, description='Product price'),
    'category': fields.String(required=False, description='Product category'),
    'is_active': fields.Boolean(required=False, description='Product active status')
})

# Task Models
task_model = api.model('Task', {
    'id': fields.Integer(required=True, description='Task ID'),
    'title': fields.String(required=True, description='Task title'),
    'description': fields.String(required=False, description='Task description'),
    'assigned_to': fields.Integer(required=True, description='Assigned salesman ID'),
    'assigned_by': fields.Integer(required=True, description='Assigned by user ID'),
    'status': fields.String(required=True, description='Task status'),
    'priority': fields.String(required=True, description='Task priority'),
    'due_date': fields.DateTime(required=False, description='Due date'),
    'progress': fields.Integer(required=True, description='Progress percentage'),
    'created_at': fields.DateTime(required=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(required=True, description='Last update timestamp')
})

task_create_model = api.model('TaskCreate', {
    'title': fields.String(required=True, description='Task title', example='Follow up with client'),
    'description': fields.String(required=False, description='Task description', example='Call the client to discuss pricing'),
    'assigned_to': fields.Integer(required=True, description='Assigned salesman ID', example=1),
    'priority': fields.String(required=True, description='Task priority', example='high'),
    'due_date': fields.DateTime(required=False, description='Due date', example='2024-12-31T23:59:59Z')
})

task_update_model = api.model('TaskUpdate', {
    'title': fields.String(required=False, description='Task title'),
    'description': fields.String(required=False, description='Task description'),
    'assigned_to': fields.Integer(required=False, description='Assigned salesman ID'),
    'status': fields.String(required=False, description='Task status'),
    'priority': fields.String(required=False, description='Task priority'),
    'due_date': fields.DateTime(required=False, description='Due date'),
    'progress': fields.Integer(required=False, description='Progress percentage')
})

# Lead Models
lead_model = api.model('Lead', {
    'id': fields.Integer(required=True, description='Lead ID'),
    'lead_id': fields.String(required=False, description='Lead ID string'),
    'name': fields.String(required=True, description='Lead name'),
    'contactNo': fields.String(required=True, description='Contact number'),
    'email': fields.String(required=True, description='Email address'),
    'productName': fields.String(required=True, description='Product name'),
    'productStatus': fields.String(required=True, description='Product status'),
    'salesman_name': fields.String(required=False, description='Assigned salesman name'),
    'status': fields.String(required=True, description='Lead status'),
    'value': fields.Float(required=True, description='Lead value'),
    'created_at': fields.DateTime(required=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(required=True, description='Last update timestamp')
})

lead_create_model = api.model('LeadCreate', {
    'name': fields.String(required=True, description='Lead name', example='John Smith'),
    'contactNo': fields.String(required=True, description='Contact number', example='+1234567890'),
    'email': fields.String(required=True, description='Email address', example='john@example.com'),
    'productName': fields.String(required=True, description='Product name', example='E-School'),
    'productStatus': fields.String(required=True, description='Product status', example='interested'),
    'salesmanName': fields.String(required=True, description='Salesman name', example='Jane Doe'),
    'status': fields.String(required=True, description='Lead status', example='active'),
    'value': fields.Float(required=True, description='Lead value', example=10000.0)
})

lead_update_model = api.model('LeadUpdate', {
    'name': fields.String(required=False, description='Lead name'),
    'contactNo': fields.String(required=False, description='Contact number'),
    'email': fields.String(required=False, description='Email address'),
    'productName': fields.String(required=False, description='Product name'),
    'productStatus': fields.String(required=False, description='Product status'),
    'salesmanName': fields.String(required=False, description='Salesman name'),
    'status': fields.String(required=False, description='Lead status'),
    'value': fields.Float(required=False, description='Lead value')
})

# Deal Models
deal_model = api.model('Deal', {
    'id': fields.Integer(required=True, description='Deal ID'),
    'lead_id': fields.Integer(required=True, description='Associated lead ID'),
    'salesman_id': fields.Integer(required=True, description='Salesman ID'),
    'product_id': fields.Integer(required=False, description='Product ID'),
    'value': fields.Float(required=True, description='Deal value'),
    'status': fields.String(required=True, description='Deal status'),
    'notes': fields.String(required=False, description='Deal notes'),
    'created_at': fields.DateTime(required=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(required=True, description='Last update timestamp')
})

deal_create_model = api.model('DealCreate', {
    'lead_id': fields.Integer(required=True, description='Associated lead ID', example=1),
    'salesman_id': fields.Integer(required=True, description='Salesman ID', example=1),
    'product_id': fields.Integer(required=False, description='Product ID', example=1),
    'value': fields.Float(required=True, description='Deal value', example=10000.0),
    'status': fields.String(required=True, description='Deal status', example='negotiation'),
    'notes': fields.String(required=False, description='Deal notes', example='Client interested in premium package')
})

deal_update_model = api.model('DealUpdate', {
    'lead_id': fields.Integer(required=False, description='Associated lead ID'),
    'salesman_id': fields.Integer(required=False, description='Salesman ID'),
    'product_id': fields.Integer(required=False, description='Product ID'),
    'value': fields.Float(required=False, description='Deal value'),
    'status': fields.String(required=False, description='Deal status'),
    'notes': fields.String(required=False, description='Deal notes')
})

# Meeting Models
meeting_model = api.model('Meeting', {
    'id': fields.Integer(required=True, description='Meeting ID'),
    'title': fields.String(required=True, description='Meeting title'),
    'description': fields.String(required=False, description='Meeting description'),
    'salesman_id': fields.Integer(required=True, description='Salesman ID'),
    'client_name': fields.String(required=True, description='Client name'),
    'client_contact': fields.String(required=True, description='Client contact'),
    'meeting_date': fields.DateTime(required=True, description='Meeting date and time'),
    'duration': fields.Integer(required=False, description='Meeting duration in minutes'),
    'status': fields.String(required=True, description='Meeting status'),
    'notes': fields.String(required=False, description='Meeting notes'),
    'created_at': fields.DateTime(required=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(required=True, description='Last update timestamp')
})

meeting_create_model = api.model('MeetingCreate', {
    'title': fields.String(required=True, description='Meeting title', example='Product Demo'),
    'description': fields.String(required=False, description='Meeting description', example='Demonstrate E-School features'),
    'client_name': fields.String(required=True, description='Client name', example='ABC School'),
    'client_contact': fields.String(required=True, description='Client contact', example='+1234567890'),
    'meeting_date': fields.DateTime(required=True, description='Meeting date and time', example='2024-12-31T14:00:00Z'),
    'duration': fields.Integer(required=False, description='Meeting duration in minutes', example=60),
    'notes': fields.String(required=False, description='Meeting notes', example='Prepare demo environment')
})

meeting_update_model = api.model('MeetingUpdate', {
    'title': fields.String(required=False, description='Meeting title'),
    'description': fields.String(required=False, description='Meeting description'),
    'client_name': fields.String(required=False, description='Client name'),
    'client_contact': fields.String(required=False, description='Client contact'),
    'meeting_date': fields.DateTime(required=False, description='Meeting date and time'),
    'duration': fields.Integer(required=False, description='Meeting duration in minutes'),
    'status': fields.String(required=False, description='Meeting status'),
    'notes': fields.String(required=False, description='Meeting notes')
})

# Response Models
success_response_model = api.model('SuccessResponse', {
    'message': fields.String(required=True, description='Success message'),
    'data': fields.Raw(required=False, description='Response data')
})

error_response_model = api.model('ErrorResponse', {
    'error': fields.String(required=True, description='Error message'),
    'details': fields.String(required=False, description='Additional error details')
})

token_response_model = api.model('TokenResponse', {
    'message': fields.String(required=True, description='Response message'),
    'access_token': fields.String(required=True, description='JWT access token'),
    'user': fields.Nested(user_model, required=True, description='User information')
})

token_verification_model = api.model('TokenVerification', {
    'valid': fields.Boolean(required=True, description='Token validity status'),
    'user': fields.Nested(user_model, required=False, description='User information')
})

health_model = api.model('Health', {
    'status': fields.String(required=True, description='API health status'),
    'timestamp': fields.DateTime(required=True, description='Health check timestamp'),
    'version': fields.String(required=True, description='API version'),
    'database': fields.String(required=True, description='Database connection status')
})

api_info_model = api.model('APIInfo', {
    'message': fields.String(required=True, description='API welcome message'),
    'version': fields.String(required=True, description='API version'),
    'endpoints': fields.Raw(required=True, description='Available API endpoints'),
    'status': fields.String(required=True, description='API status')
})

# ==================== NAMESPACES ====================

auth_ns = Namespace('Authentication', description='User authentication and authorization endpoints')
salesmen_ns = Namespace('Salesmen', description='Salesman management endpoints')
products_ns = Namespace('Products', description='Product management endpoints')
tasks_ns = Namespace('Tasks', description='Task management endpoints')
leads_ns = Namespace('Leads', description='Lead management endpoints')
deals_ns = Namespace('Deals', description='Deal management endpoints')
meetings_ns = Namespace('Meetings', description='Meeting management endpoints')
salesman_portal_ns = Namespace('Salesman Portal', description='Salesman portal endpoints')
health_ns = Namespace('Health', description='API health check endpoints')
root_ns = Namespace('Root', description='API information and root endpoints')

# Add namespaces to API
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(salesmen_ns, path='/salesmen')
api.add_namespace(products_ns, path='/products')
api.add_namespace(tasks_ns, path='/tasks')
api.add_namespace(leads_ns, path='/leads')
api.add_namespace(deals_ns, path='/deals')
api.add_namespace(meetings_ns, path='/meetings')
api.add_namespace(salesman_portal_ns, path='/salesman')
api.add_namespace(health_ns, path='/health')
api.add_namespace(root_ns, path='/')

# ==================== AUTHENTICATION ENDPOINTS ====================

@auth_ns.route('/signup')
class UserRegistration(Resource):
    @auth_ns.expect(registration_model, validate=True)
    @auth_ns.response(201, 'User created successfully', success_response_model)
    @auth_ns.response(400, 'Bad request', error_response_model)
    @auth_ns.response(409, 'User already exists', error_response_model)
    @auth_ns.response(500, 'Internal server error', error_response_model)
    def post(self):
        """
        Register a new main user
        
        Creates a new main user account with the provided information.
        The password will be securely hashed before storage.
        """
        pass

@auth_ns.route('/login')
class UserLogin(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.response(200, 'Login successful', token_response_model)
    @auth_ns.response(401, 'Invalid credentials', error_response_model)
    @auth_ns.response(400, 'Bad request', error_response_model)
    @auth_ns.response(500, 'Internal server error', error_response_model)
    def post(self):
        """
        User login
        
        Authenticates a user with email/username and password.
        Returns a JWT token for subsequent API requests.
        """
        pass

@auth_ns.route('/me')
class UserProfile(Resource):
    @auth_ns.response(200, 'User profile retrieved', user_model)
    @auth_ns.response(401, 'Unauthorized', error_response_model)
    @auth_ns.response(500, 'Internal server error', error_response_model)
    def get(self):
        """
        Get current user profile
        
        Returns the profile information of the currently authenticated user.
        Requires a valid JWT token in the Authorization header.
        """
        pass

@auth_ns.route('/verify-token')
class TokenVerification(Resource):
    @auth_ns.response(200, 'Token is valid', token_verification_model)
    @auth_ns.response(401, 'Invalid or expired token', error_response_model)
    @auth_ns.response(500, 'Internal server error', error_response_model)
    def get(self):
        """
        Verify JWT token
        
        Validates the provided JWT token and returns user information if valid.
        Requires a valid JWT token in the Authorization header.
        """
        pass

# ==================== SALESMEN ENDPOINTS ====================

@salesmen_ns.route('/')
class SalesmenList(Resource):
    @salesmen_ns.response(200, 'Salesmen retrieved successfully', api.model('SalesmenList', {
        'salesmen': fields.List(fields.Nested(user_model), required=True, description='List of salesmen')
    }))
    @salesmen_ns.response(401, 'Unauthorized', error_response_model)
    @salesmen_ns.response(403, 'Forbidden', error_response_model)
    @salesmen_ns.response(500, 'Internal server error', error_response_model)
    def get(self):
        """
        Get all salesmen
        
        Returns a list of all active salesmen for the current main user.
        Requires authentication and main user privileges.
        """
        pass

    @salesmen_ns.expect(salesman_create_model, validate=True)
    @salesmen_ns.response(201, 'Salesman created successfully', salesman_response_model)
    @salesmen_ns.response(400, 'Bad request', error_response_model)
    @salesmen_ns.response(401, 'Unauthorized', error_response_model)
    @salesmen_ns.response(500, 'Internal server error', error_response_model)
    def post(self):
        """
        Create a new salesman
        
        Creates a new salesman (sub-user) under the current main user.
        Returns the salesman information and generated login credentials.
        """
        pass

@salesmen_ns.route('/<int:salesman_id>')
class SalesmanDetail(Resource):
    @salesmen_ns.expect(salesman_update_model, validate=True)
    @salesmen_ns.response(200, 'Salesman updated successfully', success_response_model)
    @salesmen_ns.response(400, 'Bad request', error_response_model)
    @salesmen_ns.response(401, 'Unauthorized', error_response_model)
    @salesmen_ns.response(404, 'Salesman not found', error_response_model)
    @salesmen_ns.response(500, 'Internal server error', error_response_model)
    def put(self, salesman_id):
        """
        Update salesman information
        
        Updates the full information of a specific salesman.
        """
        pass

    @salesmen_ns.expect(api.model('StatusUpdate', {
        'is_active': fields.Boolean(required=True, description='Active status')
    }), validate=True)
    @salesmen_ns.response(200, 'Status updated successfully', success_response_model)
    @salesmen_ns.response(400, 'Bad request', error_response_model)
    @salesmen_ns.response(401, 'Unauthorized', error_response_model)
    @salesmen_ns.response(404, 'Salesman not found', error_response_model)
    @salesmen_ns.response(500, 'Internal server error', error_response_model)
    def patch(self, salesman_id):
        """
        Update salesman status
        
        Updates the active status of a specific salesman.
        """
        pass

    @salesmen_ns.response(200, 'Salesman deleted successfully', success_response_model)
    @salesmen_ns.response(401, 'Unauthorized', error_response_model)
    @salesmen_ns.response(404, 'Salesman not found', error_response_model)
    @salesmen_ns.response(500, 'Internal server error', error_response_model)
    def delete(self, salesman_id):
        """
        Delete salesman
        
        Soft deletes a salesman account. The salesman will be marked as inactive
        and will not appear in the active salesmen list.
        """
        pass

@salesmen_ns.route('/<int:salesman_id>/reset-password')
class SalesmanPasswordReset(Resource):
    @salesmen_ns.response(200, 'Password reset successfully', api.model('PasswordReset', {
        'message': fields.String(required=True, description='Success message'),
        'new_password': fields.String(required=True, description='New generated password')
    }))
    @salesmen_ns.response(401, 'Unauthorized', error_response_model)
    @salesmen_ns.response(404, 'Salesman not found', error_response_model)
    @salesmen_ns.response(500, 'Internal server error', error_response_model)
    def post(self, salesman_id):
        """
        Reset salesman password
        
        Generates a new random password for the specified salesman.
        """
        pass

# ==================== PRODUCTS ENDPOINTS ====================

@products_ns.route('/')
class ProductsList(Resource):
    @products_ns.response(200, 'Products retrieved successfully', api.model('ProductsList', {
        'products': fields.List(fields.Nested(product_model), required=True, description='List of products')
    }))
    @products_ns.response(401, 'Unauthorized', error_response_model)
    @products_ns.response(500, 'Internal server error', error_response_model)
    def get(self):
        """
        Get all products
        
        Returns a list of all products for the current user.
        """
        pass

    @products_ns.expect(product_create_model, validate=True)
    @products_ns.response(201, 'Product created successfully', success_response_model)
    @products_ns.response(400, 'Bad request', error_response_model)
    @products_ns.response(401, 'Unauthorized', error_response_model)
    @products_ns.response(500, 'Internal server error', error_response_model)
    def post(self):
        """
        Create a new product
        
        Creates a new product in the system.
        """
        pass

@products_ns.route('/<int:product_id>')
class ProductDetail(Resource):
    @products_ns.expect(product_update_model, validate=True)
    @products_ns.response(200, 'Product updated successfully', success_response_model)
    @products_ns.response(400, 'Bad request', error_response_model)
    @products_ns.response(401, 'Unauthorized', error_response_model)
    @products_ns.response(404, 'Product not found', error_response_model)
    @products_ns.response(500, 'Internal server error', error_response_model)
    def put(self, product_id):
        """
        Update product
        
        Updates the information of a specific product.
        """
        pass

    @products_ns.response(200, 'Product deleted successfully', success_response_model)
    @products_ns.response(401, 'Unauthorized', error_response_model)
    @products_ns.response(404, 'Product not found', error_response_model)
    @products_ns.response(500, 'Internal server error', error_response_model)
    def delete(self, product_id):
        """
        Delete product
        
        Deletes a specific product from the system.
        """
        pass

# ==================== TASKS ENDPOINTS ====================

@tasks_ns.route('/')
class TasksList(Resource):
    @tasks_ns.response(200, 'Tasks retrieved successfully', api.model('TasksList', {
        'tasks': fields.List(fields.Nested(task_model), required=True, description='List of tasks')
    }))
    @tasks_ns.response(401, 'Unauthorized', error_response_model)
    @tasks_ns.response(500, 'Internal server error', error_response_model)
    def get(self):
        """
        Get all tasks
        
        Returns a list of all tasks for the current user.
        """
        pass

    @tasks_ns.expect(task_create_model, validate=True)
    @tasks_ns.response(201, 'Task created successfully', success_response_model)
    @tasks_ns.response(400, 'Bad request', error_response_model)
    @tasks_ns.response(401, 'Unauthorized', error_response_model)
    @tasks_ns.response(500, 'Internal server error', error_response_model)
    def post(self):
        """
        Create a new task
        
        Creates a new task and assigns it to a salesman.
        """
        pass

@tasks_ns.route('/<int:task_id>')
class TaskDetail(Resource):
    @tasks_ns.expect(task_update_model, validate=True)
    @tasks_ns.response(200, 'Task updated successfully', success_response_model)
    @tasks_ns.response(400, 'Bad request', error_response_model)
    @tasks_ns.response(401, 'Unauthorized', error_response_model)
    @tasks_ns.response(404, 'Task not found', error_response_model)
    @tasks_ns.response(500, 'Internal server error', error_response_model)
    def put(self, task_id):
        """
        Update task
        
        Updates the information of a specific task.
        """
        pass

    @tasks_ns.response(200, 'Task deleted successfully', success_response_model)
    @tasks_ns.response(401, 'Unauthorized', error_response_model)
    @tasks_ns.response(404, 'Task not found', error_response_model)
    @tasks_ns.response(500, 'Internal server error', error_response_model)
    def delete(self, task_id):
        """
        Delete task
        
        Deletes a specific task from the system.
        """
        pass

# ==================== LEADS ENDPOINTS ====================

@leads_ns.route('/')
class LeadsList(Resource):
    @leads_ns.response(200, 'Leads retrieved successfully', api.model('LeadsList', {
        'leads': fields.List(fields.Nested(lead_model), required=True, description='List of leads')
    }))
    @leads_ns.response(401, 'Unauthorized', error_response_model)
    @leads_ns.response(500, 'Internal server error', error_response_model)
    def get(self):
        """
        Get all leads
        
        Returns a list of all leads for the current user.
        """
        pass

    @leads_ns.expect(lead_create_model, validate=True)
    @leads_ns.response(201, 'Lead created successfully', success_response_model)
    @leads_ns.response(400, 'Bad request', error_response_model)
    @leads_ns.response(401, 'Unauthorized', error_response_model)
    @leads_ns.response(500, 'Internal server error', error_response_model)
    def post(self):
        """
        Create a new lead
        
        Creates a new lead in the system.
        """
        pass

@leads_ns.route('/<int:lead_id>')
class LeadDetail(Resource):
    @leads_ns.expect(lead_update_model, validate=True)
    @leads_ns.response(200, 'Lead updated successfully', success_response_model)
    @leads_ns.response(400, 'Bad request', error_response_model)
    @leads_ns.response(401, 'Unauthorized', error_response_model)
    @leads_ns.response(404, 'Lead not found', error_response_model)
    @leads_ns.response(500, 'Internal server error', error_response_model)
    def put(self, lead_id):
        """
        Update lead
        
        Updates the information of a specific lead.
        """
        pass

    @leads_ns.response(200, 'Lead deleted successfully', success_response_model)
    @leads_ns.response(401, 'Unauthorized', error_response_model)
    @leads_ns.response(404, 'Lead not found', error_response_model)
    @leads_ns.response(500, 'Internal server error', error_response_model)
    def delete(self, lead_id):
        """
        Delete lead
        
        Deletes a specific lead from the system.
        """
        pass

@leads_ns.route('/<int:lead_id>/status')
class LeadStatusUpdate(Resource):
    @leads_ns.expect(api.model('StatusUpdate', {
        'status': fields.String(required=True, description='New lead status', example='Accepted')
    }), validate=True)
    @leads_ns.response(200, 'Lead status updated successfully', success_response_model)
    @leads_ns.response(400, 'Bad request', error_response_model)
    @leads_ns.response(401, 'Unauthorized', error_response_model)
    @leads_ns.response(404, 'Lead not found', error_response_model)
    @leads_ns.response(500, 'Internal server error', error_response_model)
    def patch(self, lead_id):
        """
        Update lead status
        
        Updates the status of a specific lead.
        """
        pass

# ==================== DEALS ENDPOINTS ====================

@deals_ns.route('/')
class DealsList(Resource):
    @deals_ns.response(200, 'Deals retrieved successfully', api.model('DealsList', {
        'deals': fields.List(fields.Nested(deal_model), required=True, description='List of deals')
    }))
    @deals_ns.response(401, 'Unauthorized', error_response_model)
    @deals_ns.response(500, 'Internal server error', error_response_model)
    def get(self):
        """
        Get all deals
        
        Returns a list of all deals for the current user.
        """
        pass

    @deals_ns.expect(deal_create_model, validate=True)
    @deals_ns.response(201, 'Deal created successfully', success_response_model)
    @deals_ns.response(400, 'Bad request', error_response_model)
    @deals_ns.response(401, 'Unauthorized', error_response_model)
    @deals_ns.response(500, 'Internal server error', error_response_model)
    def post(self):
        """
        Create a new deal
        
        Creates a new deal in the system.
        """
        pass

@deals_ns.route('/<int:deal_id>')
class DealDetail(Resource):
    @deals_ns.expect(deal_update_model, validate=True)
    @deals_ns.response(200, 'Deal updated successfully', success_response_model)
    @deals_ns.response(400, 'Bad request', error_response_model)
    @deals_ns.response(401, 'Unauthorized', error_response_model)
    @deals_ns.response(404, 'Deal not found', error_response_model)
    @deals_ns.response(500, 'Internal server error', error_response_model)
    def put(self, deal_id):
        """
        Update deal
        
        Updates the information of a specific deal.
        """
        pass

    @deals_ns.response(200, 'Deal deleted successfully', success_response_model)
    @deals_ns.response(401, 'Unauthorized', error_response_model)
    @deals_ns.response(404, 'Deal not found', error_response_model)
    @deals_ns.response(500, 'Internal server error', error_response_model)
    def delete(self, deal_id):
        """
        Delete deal
        
        Deletes a specific deal from the system.
        """
        pass

@deals_ns.route('/<int:deal_id>/status')
class DealStatusUpdate(Resource):
    @deals_ns.expect(api.model('StatusUpdate', {
        'status': fields.String(required=True, description='New deal status', example='WON')
    }), validate=True)
    @deals_ns.response(200, 'Deal status updated successfully', success_response_model)
    @deals_ns.response(400, 'Bad request', error_response_model)
    @deals_ns.response(401, 'Unauthorized', error_response_model)
    @deals_ns.response(404, 'Deal not found', error_response_model)
    @deals_ns.response(500, 'Internal server error', error_response_model)
    def patch(self, deal_id):
        """
        Update deal status
        
        Updates the status of a specific deal.
        """
        pass

# ==================== MEETINGS ENDPOINTS ====================

@meetings_ns.route('/')
class MeetingsList(Resource):
    @meetings_ns.response(200, 'Meetings retrieved successfully', api.model('MeetingsList', {
        'meetings': fields.List(fields.Nested(meeting_model), required=True, description='List of meetings')
    }))
    @meetings_ns.response(401, 'Unauthorized', error_response_model)
    @meetings_ns.response(500, 'Internal server error', error_response_model)
    def get(self):
        """
        Get all meetings
        
        Returns a list of all meetings for the current user.
        """
        pass

    @meetings_ns.expect(meeting_create_model, validate=True)
    @meetings_ns.response(201, 'Meeting created successfully', success_response_model)
    @meetings_ns.response(400, 'Bad request', error_response_model)
    @meetings_ns.response(401, 'Unauthorized', error_response_model)
    @meetings_ns.response(500, 'Internal server error', error_response_model)
    def post(self):
        """
        Create a new meeting
        
        Creates a new meeting in the system.
        """
        pass

@meetings_ns.route('/<int:meeting_id>')
class MeetingDetail(Resource):
    @meetings_ns.expect(meeting_update_model, validate=True)
    @meetings_ns.response(200, 'Meeting updated successfully', success_response_model)
    @meetings_ns.response(400, 'Bad request', error_response_model)
    @meetings_ns.response(401, 'Unauthorized', error_response_model)
    @meetings_ns.response(404, 'Meeting not found', error_response_model)
    @meetings_ns.response(500, 'Internal server error', error_response_model)
    def put(self, meeting_id):
        """
        Update meeting
        
        Updates the information of a specific meeting.
        """
        pass

    @meetings_ns.response(200, 'Meeting deleted successfully', success_response_model)
    @meetings_ns.response(401, 'Unauthorized', error_response_model)
    @meetings_ns.response(404, 'Meeting not found', error_response_model)
    @meetings_ns.response(500, 'Internal server error', error_response_model)
    def delete(self, meeting_id):
        """
        Delete meeting
        
        Deletes a specific meeting from the system.
        """
        pass

# ==================== SALESMAN PORTAL ENDPOINTS ====================

@salesman_portal_ns.route('/tasks')
class SalesmanTasks(Resource):
    @salesman_portal_ns.response(200, 'Tasks retrieved successfully', api.model('SalesmanTasksList', {
        'tasks': fields.List(fields.Nested(task_model), required=True, description='List of assigned tasks')
    }))
    @salesman_portal_ns.response(401, 'Unauthorized', error_response_model)
    @salesman_portal_ns.response(500, 'Internal server error', error_response_model)
    def get(self):
        """
        Get salesman tasks
        
        Returns a list of all tasks assigned to the current salesman.
        Requires salesman authentication.
        """
        pass

@salesman_portal_ns.route('/tasks/<int:task_id>/progress')
class TaskProgressUpdate(Resource):
    @salesman_portal_ns.expect(api.model('ProgressUpdate', {
        'progress': fields.Integer(required=True, description='Progress percentage (0-100)', example=75)
    }), validate=True)
    @salesman_portal_ns.response(200, 'Progress updated successfully', success_response_model)
    @salesman_portal_ns.response(400, 'Bad request', error_response_model)
    @salesman_portal_ns.response(401, 'Unauthorized', error_response_model)
    @salesman_portal_ns.response(404, 'Task not found', error_response_model)
    @salesman_portal_ns.response(500, 'Internal server error', error_response_model)
    def patch(self, task_id):
        """
        Update task progress
        
        Updates the progress of a specific task assigned to the current salesman.
        """
        pass

# ==================== SALESMAN UPDATES ENDPOINTS ====================

@root_ns.route('/salesman-updates')
class SalesmanUpdates(Resource):
    @root_ns.response(200, 'Updates retrieved successfully', api.model('SalesmanUpdates', {
        'updates': fields.List(fields.Raw(), required=True, description='List of salesman updates')
    }))
    @root_ns.response(401, 'Unauthorized', error_response_model)
    @root_ns.response(403, 'Forbidden', error_response_model)
    @root_ns.response(500, 'Internal server error', error_response_model)
    def get(self):
        """
        Get salesman updates
        
        Returns updates from all salesmen for the main user.
        Requires main user authentication.
        """
        pass

# ==================== HEALTH & ROOT ENDPOINTS ====================

@health_ns.route('/')
class HealthCheck(Resource):
    @health_ns.response(200, 'API is healthy', health_model)
    def get(self):
        """
        API Health Check
        
        Returns the current health status of the API and its dependencies.
        """
        pass

@root_ns.route('/')
class RootInfo(Resource):
    @root_ns.response(200, 'API information', api_info_model)
    def get(self):
        """
        API Root Information
        
        Returns basic information about the API including available endpoints.
        """
        pass
