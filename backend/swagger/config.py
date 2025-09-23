"""
Swagger Configuration for CRM LaitusNeo API
"""

SWAGGER_CONFIG = {
    'title': 'CRM LaitusNeo API',
    'version': '1.0.0',
    'description': '''
    # CRM LaitusNeo API Documentation
    
    A comprehensive Customer Relationship Management system API built with Flask.
    
    ## Features
    - User Authentication & Authorization
    - JWT Token Management
    - User Registration & Login
    - Secure Password Hashing
    - CORS Support
    
    ## Authentication
    This API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:
    ```
    Authorization: Bearer <your_jwt_token>
    ```
    
    ## Base URL
    ```
    http://localhost:5000/api
    ```
    
    ## Contact
    - **Developer**: LaitusNeo Team
    - **Email**: support@laitusneo.com
    ''',
    'contact': {
        'name': 'LaitusNeo Support',
        'email': 'support@laitusneo.com'
    },
    'license': {
        'name': 'MIT License',
        'url': 'https://opensource.org/licenses/MIT'
    },
    'servers': [
        {
            'url': 'http://localhost:5000',
            'description': 'Development server'
        }
    ],
    'tags': [
        {
            'name': 'Authentication',
            'description': 'User authentication and authorization endpoints'
        },
        {
            'name': 'Health',
            'description': 'API health check endpoints'
        },
        {
            'name': 'Root',
            'description': 'API information and root endpoints'
        }
    ],
    'securityDefinitions': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
        }
    },
    'security': [
        {
            'Bearer': []
        }
    ]
}
