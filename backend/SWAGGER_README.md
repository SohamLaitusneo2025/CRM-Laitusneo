# CRM LaitusNeo API Documentation

## 🚀 Quick Start

### 1. Start the API Server
```bash
cd backend
python start_swagger.py
```

### 2. Access Swagger UI
Open your browser and navigate to:
**🌐 http://localhost:5000/api/docs/**

## 📚 API Documentation Overview

The CRM LaitusNeo API provides comprehensive documentation through Swagger UI, covering all endpoints and data models.

### 🔗 Base URL
```
http://localhost:5000/api
```

### 🔐 Authentication
All protected endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## 📋 API Endpoints

### 🔑 Authentication (`/api/auth/`)
- `POST /api/auth/signup` - Register a new main user
- `POST /api/auth/login` - User login (main user or salesman)
- `GET /api/auth/me` - Get current user profile
- `GET /api/auth/verify-token` - Verify JWT token

### 👥 Salesmen Management (`/api/salesmen/`)
- `GET /api/salesmen` - Get all active salesmen
- `POST /api/salesmen` - Create a new salesman
- `PUT /api/salesmen/{id}` - Update salesman information
- `PATCH /api/salesmen/{id}` - Update salesman status
- `DELETE /api/salesmen/{id}` - Delete salesman
- `POST /api/salesmen/{id}/reset-password` - Reset salesman password

### 📦 Products (`/api/products/`)
- `GET /api/products` - Get all products
- `POST /api/products` - Create a new product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

### ✅ Tasks (`/api/tasks/`)
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### 🎯 Leads (`/api/leads/`)
- `GET /api/leads` - Get all leads
- `POST /api/leads` - Create a new lead
- `PUT /api/leads/{id}` - Update lead
- `DELETE /api/leads/{id}` - Delete lead
- `PATCH /api/leads/{id}/status` - Update lead status

### 💰 Deals (`/api/deals/`)
- `GET /api/deals` - Get all deals
- `POST /api/deals` - Create a new deal
- `PUT /api/deals/{id}` - Update deal
- `DELETE /api/deals/{id}` - Delete deal
- `PATCH /api/deals/{id}/status` - Update deal status

### 📅 Meetings (`/api/meetings/`)
- `GET /api/meetings` - Get all meetings
- `POST /api/meetings` - Create a new meeting
- `PUT /api/meetings/{id}` - Update meeting
- `DELETE /api/meetings/{id}` - Delete meeting

### 🏢 Salesman Portal (`/api/salesman/`)
- `GET /api/salesman/tasks` - Get assigned tasks
- `PATCH /api/salesman/tasks/{id}/progress` - Update task progress

### 📊 Updates (`/api/salesman-updates`)
- `GET /api/salesman-updates` - Get updates from all salesmen

### 🏥 Health Check (`/api/health`)
- `GET /api/health` - API health status

## 🎯 User Types

### Main User
- Full access to all features
- Can create and manage salesmen
- Can view all data across the system

### Sub User (Salesman)
- Limited access to assigned tasks and leads
- Can update task progress
- Can view their own data only

## 📝 Data Models

The API includes comprehensive data models for:
- **User**: User information and authentication
- **Salesman**: Salesman-specific data
- **Product**: Product catalog information
- **Task**: Task management and assignment
- **Lead**: Lead tracking and management
- **Deal**: Deal management and status tracking
- **Meeting**: Meeting scheduling and management

## 🔧 Testing the API

### 1. Using Swagger UI
1. Open http://localhost:5000/api/docs/
2. Click "Authorize" button
3. Enter your JWT token: `Bearer <your_token>`
4. Test any endpoint directly from the interface

### 2. Using cURL
```bash
# Login to get token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123", "userType": "main"}'

# Use token for authenticated requests
curl -X GET http://localhost:5000/api/salesmen \
  -H "Authorization: Bearer <your_jwt_token>"
```

### 3. Using Postman
1. Import the API collection from Swagger UI
2. Set up environment variables for base URL and token
3. Test all endpoints with proper authentication

## 🚨 Error Handling

The API returns standardized error responses:
```json
{
  "error": "Error message",
  "details": "Additional error details (optional)"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `500` - Internal Server Error

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Input validation
- SQL injection protection
- Role-based access control

## 📞 Support

For API support and questions:
- **Email**: support@laitusneo.com
- **Documentation**: http://localhost:5000/api/docs/

---

**Happy API Testing! 🎉**
