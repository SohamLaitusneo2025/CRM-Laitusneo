#!/usr/bin/env python3
"""
Start the CRM LaitusNeo API server with Swagger UI
"""

import os
import sys
from app import create_app

def main():
    """Start the Flask application"""
    app = create_app()
    
    print("=" * 60)
    print("🚀 CRM LaitusNeo API Server Starting...")
    print("=" * 60)
    print()
    print("📚 Swagger UI Documentation:")
    print("   🌐 http://localhost:5000/api/docs/")
    print()
    print("🔗 API Base URL:")
    print("   🌐 http://localhost:5000/api")
    print()
    print("📋 Available Endpoints:")
    print("   • Authentication: /api/auth/*")
    print("   • Salesmen: /api/salesmen/*")
    print("   • Products: /api/products/*")
    print("   • Tasks: /api/tasks/*")
    print("   • Leads: /api/leads/*")
    print("   • Deals: /api/deals/*")
    print("   • Meetings: /api/meetings/*")
    print("   • Salesman Portal: /api/salesman/*")
    print("   • Health Check: /api/health")
    print()
    print("🔐 Authentication:")
    print("   Use JWT tokens in Authorization header:")
    print("   Authorization: Bearer <your_jwt_token>")
    print()
    print("=" * 60)
    print("✅ Server is running! Press Ctrl+C to stop.")
    print("=" * 60)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
