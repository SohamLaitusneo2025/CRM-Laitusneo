"""
API Schemas for Swagger Documentation
"""

from flask_restx import fields

# User Schemas
user_schema = {
    'id': fields.Integer(required=True, description='User ID'),
    'email': fields.String(required=True, description='User email address'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'is_active': fields.Boolean(required=True, description='User active status'),
    'created_at': fields.DateTime(required=True, description='User creation timestamp'),
    'updated_at': fields.DateTime(required=True, description='User last update timestamp')
}

# Registration Schema
registration_schema = {
    'email': fields.String(required=True, description='User email address', example='user@example.com'),
    'password': fields.String(required=True, description='User password (min 6 characters)', example='password123'),
    'firstName': fields.String(required=True, description='User first name', example='John'),
    'lastName': fields.String(required=True, description='User last name', example='Doe')
}

# Login Schema
login_schema = {
    'email': fields.String(required=True, description='User email address', example='user@example.com'),
    'password': fields.String(required=True, description='User password', example='password123'),
    'userType': fields.String(required=False, description='User type (optional)', example='admin')
}

# Success Response Schema
success_response_schema = {
    'message': fields.String(required=True, description='Success message'),
    'user': fields.Nested(user_schema, required=False, description='User information')
}

# Error Response Schema
error_response_schema = {
    'error': fields.String(required=True, description='Error message'),
    'details': fields.String(required=False, description='Additional error details')
}

# Token Verification Schema
token_verification_schema = {
    'valid': fields.Boolean(required=True, description='Token validity status'),
    'user': fields.Nested(user_schema, required=False, description='User information')
}

# API Info Schema
api_info_schema = {
    'message': fields.String(required=True, description='API welcome message'),
    'version': fields.String(required=True, description='API version'),
    'endpoints': fields.Raw(required=True, description='Available API endpoints'),
    'status': fields.String(required=True, description='API status')
}

# Health Check Schema
health_schema = {
    'status': fields.String(required=True, description='API health status'),
    'timestamp': fields.DateTime(required=True, description='Health check timestamp'),
    'version': fields.String(required=True, description='API version'),
    'database': fields.String(required=True, description='Database connection status')
}
