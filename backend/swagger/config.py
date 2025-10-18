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
    - **User Management**: Main users and sub-users (salesmen) with role-based access
    - **Authentication & Authorization**: JWT-based secure authentication
    - **Salesman Management**: Create, update, and manage salesman accounts
    - **Product Management**: Manage product catalog and pricing
    - **Task Management**: Assign and track tasks for salesmen
    - **Lead Management**: Track and manage sales leads
    - **Deal Management**: Manage sales deals and opportunities
    - **Meeting Management**: Schedule and track client meetings
    - **Salesman Portal**: Dedicated portal for salesmen to manage their tasks
    - **Real-time Updates**: Get updates from all salesmen
    
    ## Authentication
    This API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:
    ```
    Authorization: Bearer <your_jwt_token>
    ```
    
    ## User Types
    - **Main User**: Full access to all features, can manage salesmen
    - **Sub User (Salesman)**: Limited access to assigned tasks and leads
    
    ## Base URL
    ```
    http://localhost:5000/api
    ```
    
    ## API Endpoints Overview
    - **Authentication**: `/api/auth/*` - User login, registration, profile
    - **Salesmen**: `/api/salesmen/*` - Salesman management
    - **Products**: `/api/products/*` - Product management
    - **Tasks**: `/api/tasks/*` - Task management
    - **Leads**: `/api/leads/*` - Lead management
    - **Deals**: `/api/deals/*` - Deal management
    - **Meetings**: `/api/meetings/*` - Meeting management
    - **Salesman Portal**: `/api/salesman/*` - Salesman-specific endpoints
    - **Health**: `/api/health` - API health check
    
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
            'name': 'Salesmen',
            'description': 'Salesman management endpoints'
        },
        {
            'name': 'Products',
            'description': 'Product management endpoints'
        },
        {
            'name': 'Tasks',
            'description': 'Task management endpoints'
        },
        {
            'name': 'Leads',
            'description': 'Lead management endpoints'
        },
        {
            'name': 'Deals',
            'description': 'Deal management endpoints'
        },
        {
            'name': 'Meetings',
            'description': 'Meeting management endpoints'
        },
        {
            'name': 'Salesman Portal',
            'description': 'Salesman portal endpoints'
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
