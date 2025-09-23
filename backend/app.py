from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.exceptions import BadRequest
import re
import secrets
import string
from datetime import datetime, timedelta

from config import Config
from models import db, User, Product, Task, Lead, Deal, Meeting
from swagger.api import swagger_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, origins=['http://localhost:3000'])  # React dev server
    
    # Register Swagger Blueprint
    app.register_blueprint(swagger_bp)
    
    # Configure JWT
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=3600)
    
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Helper functions
    def generate_username(prefix='SM'):
        """Generate a unique salesman username like SM1234"""
        while True:
            number = secrets.randbelow(9000) + 1000  # 1000-9999
            candidate = f"{prefix}{number}"
            if not User.query.filter_by(username=candidate).first():
                return candidate

    def generate_strong_password(length=10):
        """Generate a strong random password"""
        alphabet = string.ascii_letters + string.digits + '!@#$%'

        def meets_requirements(pwd):
            return (
                len(pwd) >= 8
                and any(c.islower() for c in pwd)
                and any(c.isupper() for c in pwd)
                and any(c.isdigit() for c in pwd)
            )

        while True:
            pwd = ''.join(secrets.choice(alphabet) for _ in range(length))
            if meets_requirements(pwd):
                return pwd

    # Validation functions
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(password):
        # At least 8 characters, 1 uppercase, 1 lowercase, 1 digit
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        return True, "Valid password"
    
    # Routes
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'message': 'CRM LaitusNeo API Server',
            'version': '1.0.0',
            'endpoints': {
                'health': 'GET /api/health',
                'auth': {
                    'signup': 'POST /api/auth/signup',
                    'login': 'POST /api/auth/login',
                    'me': 'GET /api/auth/me',
                    'verify_token': 'GET /api/auth/verify-token'
                },
                'salesmen': {
                    'create': 'POST /api/salesmen',
                    'list': 'GET /api/salesmen',
                    'update': 'PUT /api/salesmen/<id>',
                    'update_status': 'PATCH /api/salesmen/<id>',
                    'reset_password': 'POST /api/salesmen/<id>/reset-password',
                    'delete': 'DELETE /api/salesmen/<id>'
                },
                'products': {
                    'create': 'POST /api/products',
                    'list': 'GET /api/products',
                    'update': 'PUT /api/products/<id>',
                    'delete': 'DELETE /api/products/<id>'
                },
                'tasks': {
                    'create': 'POST /api/tasks',
                    'list': 'GET /api/tasks',
                    'update': 'PUT /api/tasks/<id>',
                    'delete': 'DELETE /api/tasks/<id>'
                },
                'salesman_portal': {
                    'get_tasks': 'GET /api/salesman/tasks',
                    'update_progress': 'PATCH /api/salesman/tasks/<id>/progress'
                },
                'deals': {
                    'create': 'POST /api/deals',
                    'list': 'GET /api/deals',
                    'update': 'PUT /api/deals/<id>',
                    'delete': 'DELETE /api/deals/<id>',
                    'update_status': 'PATCH /api/deals/<id>/status'
                },
                'salesman_updates': {
                    'get_updates': 'GET /api/salesman-updates'
                }
            },
            'status': 'running'
        })
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        try:
            # Test database connection
            db.session.execute('SELECT 1')
            return jsonify({
                'status': 'healthy', 
                'message': 'CRM API is running',
                'database': 'connected'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'unhealthy', 
                'message': 'CRM API is running but database connection failed',
                'database': 'disconnected',
                'error': str(e)
            }), 500
    
    @app.route('/api/auth/signup', methods=['POST'])
    def signup():
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['email', 'password', 'firstName', 'lastName']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400
            
            email = data['email'].lower().strip()
            password = data['password']
            first_name = data['firstName'].strip()
            last_name = data['lastName'].strip()
            
            # Validate email format
            if not validate_email(email):
                return jsonify({'error': 'Invalid email format'}), 400
            
            # Validate password strength
            is_valid_password, password_message = validate_password(password)
            if not is_valid_password:
                return jsonify({'error': password_message}), 400
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({'error': 'User with this email already exists'}), 409
            
            # Create new user (only main users can sign up)
            new_user = User(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type='main'
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            # Create access token
            access_token = create_access_token(
                identity=new_user.id,
                expires_delta=timedelta(seconds=3600)
            )
            
            return jsonify({
                'message': 'User created successfully',
                'access_token': access_token,
                'user': new_user.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        try:
            data = request.get_json()
            
            # Validate required fields
            if not data.get('password'):
                return jsonify({'error': 'Password is required'}), 400

            user_type = data.get('userType', 'main')  # Default to main user
            password = data['password']
            email = (data.get('email') or '').lower().strip()
            username = (data.get('username') or '').strip()

            # Determine lookup mode
            user = None
            if user_type == 'sub' and username:
                # Sub-user can log in with username
                user = User.query.filter_by(username=username, user_type='sub').first()
            else:
                # Fallback to email (validate when provided)
                if not email:
                    return jsonify({'error': 'Email is required for main user login'}), 400
                if not validate_email(email):
                    return jsonify({'error': 'Invalid email format'}), 400
                user = User.query.filter_by(email=email, user_type=user_type).first()

            if not user or not user.check_password(password):
                return jsonify({'error': 'Invalid credentials'}), 401
            
            if not user.is_active:
                return jsonify({'error': 'Account is deactivated'}), 401
            
            # Create access token
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(seconds=3600)
            )
            
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'user': user.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    
    @app.route('/api/auth/me', methods=['GET'])
    @jwt_required()
    def get_current_user():
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({'user': user.to_dict()}), 200
            
        except Exception as e:
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    
    @app.route('/api/auth/verify-token', methods=['GET'])
    @jwt_required()
    def verify_token():
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user or not user.is_active:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            return jsonify({
                'valid': True,
                'user': user.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'error': 'Token verification failed', 'details': str(e)}), 401
    
    # Salesmen management (sub-users)
    @app.route('/api/salesmen', methods=['POST'])
    @jwt_required()
    def create_salesman():
        """Create a sub-user (salesman) under the current main user"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'main':
                return jsonify({'error': 'Only main users can create salesmen'}), 403

            data = request.get_json() or {}

            # Validate required fields
            name = (data.get('name') or '').strip()
            email = (data.get('email') or '').lower().strip()
            contact_number = (data.get('contactNumber') or '').strip()
            if not name or not email:
                return jsonify({'error': 'name and email are required'}), 400
            if not validate_email(email):
                return jsonify({'error': 'Invalid email format'}), 400

            # Check if email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({'error': 'User with this email already exists'}), 409

            # Parse name into first/last
            parts = name.split(' ', 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ''

            # Generate or use provided username/password
            desired_username = (data.get('username') or '').strip()
            if desired_username:
                # Ensure uniqueness
                if User.query.filter_by(username=desired_username).first():
                    return jsonify({'error': 'Username already exists'}), 409
                username = desired_username
            else:
                username = generate_username()

            plain_password = (data.get('password') or '').strip()
            if not plain_password:
                plain_password = generate_strong_password()

            # Create sub-user
            new_user = User(
                email=email,
                password=plain_password,
                first_name=first_name,
                last_name=last_name,
                user_type='sub',
                main_user_id=current_user.id,
                username=username,
                contact_number=contact_number
            )
            db.session.add(new_user)
            db.session.commit()

            return jsonify({
                'message': 'Salesman created successfully',
                'user': new_user.to_dict(),
                'credentials': {
                    'username': username,
                    'password': plain_password  # Return plain password only once
                }
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/salesmen', methods=['GET'])
    @jwt_required()
    def list_salesmen():
        """List sub-users (salesmen) for the current main user. Includes both active and inactive users."""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'main':
                return jsonify({'error': 'Only main users can view salesmen'}), 403

            subs = (
                User.query
                .filter_by(main_user_id=current_user.id, user_type='sub')
                .order_by(User.created_at.desc())
                .all()
            )
            return jsonify({
                'salesmen': [u.to_dict() for u in subs]
            }), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/salesmen/<int:salesman_id>', methods=['PATCH'])
    @jwt_required()
    def update_salesman_status(salesman_id):
        """Update a salesman's status"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'main':
                return jsonify({'error': 'Only main users can update salesmen'}), 403

            salesman = User.query.filter_by(id=salesman_id, main_user_id=current_user.id, user_type='sub').first()
            if not salesman:
                return jsonify({'error': 'Salesman not found'}), 404

            data = request.get_json() or {}
            if 'is_active' in data:
                salesman.is_active = data['is_active']
                salesman.updated_at = datetime.utcnow()
                db.session.commit()

            return jsonify({
                'message': 'Salesman updated successfully',
                'user': salesman.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/salesmen/<int:salesman_id>', methods=['PUT'])
    @jwt_required()
    def update_salesman(salesman_id):
        """Update a salesman's full information"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'main':
                return jsonify({'error': 'Only main users can update salesmen'}), 403

            salesman = User.query.filter_by(id=salesman_id, main_user_id=current_user.id, user_type='sub').first()
            if not salesman:
                return jsonify({'error': 'Salesman not found'}), 404

            data = request.get_json() or {}
            
            # Validate required fields
            if 'first_name' in data and not data['first_name'].strip():
                return jsonify({'error': 'First name is required'}), 400
            if 'last_name' in data and not data['last_name'].strip():
                return jsonify({'error': 'Last name is required'}), 400
            if 'email' in data and not data['email'].strip():
                return jsonify({'error': 'Email is required'}), 400
            if 'contact_number' in data and not data['contact_number'].strip():
                return jsonify({'error': 'Contact number is required'}), 400

            # Validate email format if provided
            if 'email' in data:
                email = data['email'].lower().strip()
                if not validate_email(email):
                    return jsonify({'error': 'Invalid email format'}), 400
                
                # Check if email is already taken by another user
                existing_user = User.query.filter(User.email == email, User.id != salesman_id).first()
                if existing_user:
                    return jsonify({'error': 'Email already exists'}), 409

            # Update fields
            if 'first_name' in data:
                salesman.first_name = data['first_name'].strip()
            if 'last_name' in data:
                salesman.last_name = data['last_name'].strip()
            if 'email' in data:
                salesman.email = email
            if 'contact_number' in data:
                salesman.contact_number = data['contact_number'].strip()
            if 'is_active' in data:
                salesman.is_active = data['is_active']
            
            salesman.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Salesman updated successfully',
                'user': salesman.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/salesmen/<int:salesman_id>', methods=['DELETE'])
    @jwt_required()
    def delete_salesman(salesman_id):
        """Delete a salesman and their assigned tasks to satisfy FK constraints"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'main':
                return jsonify({'error': 'Only main users can delete salesmen'}), 403

            salesman = User.query.filter_by(id=salesman_id, main_user_id=current_user.id, user_type='sub').first()
            if not salesman:
                return jsonify({'error': 'Salesman not found'}), 404

            # Delete tasks referencing this user (as salesman or assigner) row-by-row for maximum compatibility
            try:
                tasks_to_delete = Task.query.filter(
                    (Task.salesman_id == salesman.id) | (Task.assigned_by_id == salesman.id)
                ).all()
                for t in tasks_to_delete:
                    db.session.delete(t)
                db.session.commit()  # commit task deletions first to clear FKs
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'Failed to delete related tasks', 'details': str(e)}), 500

            # Soft-delete the salesman to avoid unique/relational edge-cases while removing from UI
            try:
                original_email = salesman.email or f'user{salesman.id}@deleted.local'
                original_username = salesman.username or f'user{salesman.id}'
                salesman.is_active = False
                # Ensure unique constraints are preserved after soft delete
                salesman.email = f"deleted_{salesman.id}_{original_email}"
                salesman.username = f"deleted_{salesman.id}_{original_username}"
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                # If soft-delete update fails, attempt hard delete as a fallback
                try:
                    db.session.delete(salesman)
                    db.session.commit()
                except Exception as e2:
                    db.session.rollback()
                    return jsonify({'error': 'Failed to delete salesman', 'details': str(e2)}), 500

            return jsonify({
                'message': 'Salesman deleted successfully'
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/salesmen/<int:salesman_id>/reset-password', methods=['POST'])
    @jwt_required()
    def reset_salesman_password(salesman_id):
        """Reset a salesman's password"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'main':
                return jsonify({'error': 'Only main users can reset salesman passwords'}), 403

            salesman = User.query.filter_by(id=salesman_id, main_user_id=current_user.id, user_type='sub').first()
            if not salesman:
                return jsonify({'error': 'Salesman not found'}), 404

            # Generate new password
            new_password = generate_strong_password()
            
            # Update salesman's password
            salesman.password_hash = salesman.hash_password(new_password)
            salesman.updated_at = datetime.utcnow()
            
            db.session.commit()

            return jsonify({
                'message': 'Password reset successfully',
                'new_password': new_password,
                'salesman': {
                    'id': salesman.id,
                    'username': salesman.username,
                    'name': f"{salesman.first_name} {salesman.last_name}"
                }
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    # Product management APIs
    @app.route('/api/products', methods=['POST'])
    @jwt_required()
    def create_product():
        """Create a new product"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'main':
                return jsonify({'error': 'Only main users can create products'}), 403

            data = request.get_json() or {}
            
            # Validate required fields
            name = (data.get('name') or '').strip()
            if not name:
                return jsonify({'error': 'Product name is required'}), 400

            # Create new product
            new_product = Product(
                name=name,
                description=data.get('description', '').strip(),
                price=data.get('price', '').strip(),
                delivery_timeline=data.get('deliveryTimeline', '').strip(),
                technologies=data.get('technologies', '').strip(),
                github_link=data.get('githubLink', '').strip(),
                preview_link=data.get('previewLink', '').strip(),
                ppt_link=data.get('pptLink', '').strip(),
                demo_video_link=data.get('demoVideoLink', '').strip(),
                admin_name=data.get('adminName', '').strip(),
                conversation_flow_link=data.get('conversationFlowLink', '').strip(),
                status=data.get('status', 'working'),
                main_user_id=current_user.id
            )
            
            db.session.add(new_product)
            db.session.commit()

            return jsonify({
                'message': 'Product created successfully',
                'product': new_product.to_dict()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/products', methods=['GET'])
    @jwt_required()
    def list_products():
        """List products for the current user (main users see their own products, sub-users see their main user's products)"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            # Determine which user's products to show
            if current_user.user_type == 'main':
                # Main user sees their own products
                products = Product.query.filter_by(main_user_id=current_user.id).order_by(Product.created_at.desc()).all()
            elif current_user.user_type == 'sub':
                # Sub-user sees products of their main user
                if not current_user.main_user_id:
                    return jsonify({'error': 'Sub-user not associated with a main user'}), 400
                products = Product.query.filter_by(main_user_id=current_user.main_user_id).order_by(Product.created_at.desc()).all()
            else:
                return jsonify({'error': 'Invalid user type'}), 400

            return jsonify({
                'products': [p.to_dict() for p in products]
            }), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/products/<int:product_id>', methods=['PUT'])
    @jwt_required()
    def update_product(product_id):
        """Update a product"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'main':
                return jsonify({'error': 'Only main users can update products'}), 403

            product = Product.query.filter_by(id=product_id, main_user_id=current_user.id).first()
            if not product:
                return jsonify({'error': 'Product not found'}), 404

            data = request.get_json() or {}
            
            # Update fields
            if 'name' in data:
                product.name = data['name'].strip()
            if 'description' in data:
                product.description = data['description'].strip()
            if 'price' in data:
                product.price = data['price'].strip()
            if 'deliveryTimeline' in data:
                product.delivery_timeline = data['deliveryTimeline'].strip()
            if 'technologies' in data:
                product.technologies = data['technologies'].strip()
            if 'githubLink' in data:
                product.github_link = data['githubLink'].strip()
            if 'previewLink' in data:
                product.preview_link = data['previewLink'].strip()
            if 'pptLink' in data:
                product.ppt_link = data['pptLink'].strip()
            if 'demoVideoLink' in data:
                product.demo_video_link = data['demoVideoLink'].strip()
            if 'adminName' in data:
                product.admin_name = data['adminName'].strip()
            if 'conversationFlowLink' in data:
                product.conversation_flow_link = data['conversationFlowLink'].strip()
            if 'status' in data:
                product.status = data['status']
            
            product.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Product updated successfully',
                'product': product.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/products/<int:product_id>', methods=['DELETE'])
    @jwt_required()
    def delete_product(product_id):
        """Delete a product"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'main':
                return jsonify({'error': 'Only main users can delete products'}), 403

            product = Product.query.filter_by(id=product_id, main_user_id=current_user.id).first()
            if not product:
                return jsonify({'error': 'Product not found'}), 404

            db.session.delete(product)
            db.session.commit()

            return jsonify({
                'message': 'Product deleted successfully'
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    # Task assignment APIs
    def generate_task_id():
        """Generate a unique task ID like T001, T002, etc."""
        last_task = Task.query.order_by(Task.id.desc()).first()
        if last_task and last_task.task_id:
            try:
                last_number = int(last_task.task_id[1:])  # Extract number from T001
                next_number = last_number + 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1
        return f"T{next_number:03d}"

    def generate_lead_id():
        """Generate a unique lead ID like L001, L002, etc."""
        try:
            # First, try to find the highest lead_id
            leads_with_id = Lead.query.filter(Lead.lead_id.isnot(None)).order_by(Lead.lead_id.desc()).first()
            if leads_with_id and leads_with_id.lead_id:
                try:
                    last_number = int(leads_with_id.lead_id[1:])  # Extract number from L001
                    next_number = last_number + 1
                except (ValueError, IndexError):
                    next_number = 1
            else:
                # Fallback: count all leads and add 1
                total_leads = Lead.query.count()
                next_number = total_leads + 1
            return f"L{next_number:03d}"
        except Exception as e:
            # If there's any error, just use a simple counter
            total_leads = Lead.query.count()
            return f"L{total_leads + 1:03d}"

    @app.route('/api/tasks', methods=['POST'])
    @jwt_required()
    def create_task():
        """Assign a new task to a salesman"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'main':
                return jsonify({'error': 'Only main users can assign tasks'}), 403

            data = request.get_json() or {}
            
            # Validate required fields
            salesman_id = data.get('salesman_id')
            product_id = data.get('product_id')
            target_quantity = data.get('target_quantity')
            due_date_str = data.get('due_date')
            title = (data.get('title') or '').strip()
            description = (data.get('description') or '').strip()
            priority = data.get('priority', 'medium')

            if not all([salesman_id, product_id, target_quantity, due_date_str, title]):
                return jsonify({'error': 'salesman_id, product_id, target_quantity, due_date, and title are required'}), 400

            # Validate salesman belongs to current user
            salesman = User.query.filter_by(id=salesman_id, main_user_id=current_user.id, user_type='sub').first()
            if not salesman:
                return jsonify({'error': 'Invalid salesman'}), 400

            # Validate product belongs to current user
            product = Product.query.filter_by(id=product_id, main_user_id=current_user.id).first()
            if not product:
                return jsonify({'error': 'Invalid product'}), 400

            # Parse due date
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid due date format. Use YYYY-MM-DD'}), 400

            # Validate target quantity
            try:
                target_quantity = int(target_quantity)
                if target_quantity <= 0:
                    return jsonify({'error': 'Target quantity must be positive'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid target quantity'}), 400

            # Generate unique task ID
            task_id = generate_task_id()

            # Create new task
            new_task = Task(
                task_id=task_id,
                title=title,
                description=description,
                target_quantity=target_quantity,
                due_date=due_date,
                priority=priority,
                salesman_id=salesman_id,
                product_id=product_id,
                assigned_by_id=current_user.id
            )
            
            db.session.add(new_task)
            db.session.commit()

            return jsonify({
                'message': 'Task assigned successfully',
                'task': new_task.to_dict()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/tasks', methods=['GET'])
    @jwt_required()
    def list_tasks():
        """List tasks for the current main user (assigned tasks)"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'main':
                return jsonify({'error': 'Only main users can view assigned tasks'}), 403

            # Get all tasks assigned by this main user
            tasks = Task.query.filter_by(assigned_by_id=current_user.id).order_by(Task.created_at.desc()).all()
            
            # Update task status based on due date
            today = datetime.utcnow().date()
            for task in tasks:
                if task.due_date < today and task.status not in ['completed']:
                    task.status = 'overdue'
            
            db.session.commit()

            return jsonify({
                'tasks': [t.to_dict() for t in tasks]
            }), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/tasks/<int:task_id>', methods=['PUT'])
    @jwt_required()
    def update_task(task_id):
        """Update a task (main user can update task details, salesman can update progress)"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            task = Task.query.get(task_id)
            if not task:
                return jsonify({'error': 'Task not found'}), 404

            data = request.get_json() or {}

            # Check permissions
            if current_user.user_type == 'main':
                # Main user can update task details
                if task.assigned_by_id != current_user.id:
                    return jsonify({'error': 'You can only update tasks you assigned'}), 403
                
                # Update task details
                if 'title' in data:
                    task.title = data['title'].strip()
                if 'description' in data:
                    task.description = data['description'].strip()
                if 'target_quantity' in data:
                    try:
                        task.target_quantity = int(data['target_quantity'])
                    except (ValueError, TypeError):
                        return jsonify({'error': 'Invalid target quantity'}), 400
                if 'due_date' in data:
                    try:
                        task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
                    except ValueError:
                        return jsonify({'error': 'Invalid due date format. Use YYYY-MM-DD'}), 400
                if 'priority' in data:
                    task.priority = data['priority']
                if 'status' in data:
                    task.status = data['status']

            elif current_user.user_type == 'sub':
                # Salesman can only update their own task progress
                if task.salesman_id != current_user.id:
                    return jsonify({'error': 'You can only update your own tasks'}), 403
                
                # Update progress
                if 'current_quantity' in data:
                    try:
                        current_quantity = int(data['current_quantity'])
                        if current_quantity < 0:
                            return jsonify({'error': 'Current quantity cannot be negative'}), 400
                        task.current_quantity = current_quantity
                        
                        # Auto-update status based on progress
                        if current_quantity >= task.target_quantity:
                            task.status = 'completed'
                        elif current_quantity > 0:
                            task.status = 'in_progress'
                        else:
                            task.status = 'pending'
                    except (ValueError, TypeError):
                        return jsonify({'error': 'Invalid current quantity'}), 400
                
                if 'status' in data:
                    task.status = data['status']
            else:
                return jsonify({'error': 'Invalid user type'}), 403

            # Update task status based on due date
            today = datetime.utcnow().date()
            if task.due_date < today and task.status not in ['completed']:
                task.status = 'overdue'

            task.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Task updated successfully',
                'task': task.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
    @jwt_required()
    def delete_task(task_id):
        """Delete a task"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'main':
                return jsonify({'error': 'Only main users can delete tasks'}), 403

            task = Task.query.get(task_id)
            if not task:
                return jsonify({'error': 'Task not found'}), 404

            if task.assigned_by_id != current_user.id:
                return jsonify({'error': 'You can only delete tasks you assigned'}), 403

            db.session.delete(task)
            db.session.commit()

            return jsonify({
                'message': 'Task deleted successfully'
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/tasks/<int:task_id>/status', methods=['PATCH'])
    @jwt_required()
    def update_task_status(task_id):
        """Update task status"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'main':
                return jsonify({'error': 'Only main users can update task status'}), 403

            task = Task.query.get(task_id)
            if not task:
                return jsonify({'error': 'Task not found'}), 404

            if task.assigned_by_id != current_user.id:
                return jsonify({'error': 'You can only update tasks you assigned'}), 403

            data = request.get_json()
            if not data or 'status' not in data:
                return jsonify({'error': 'Status is required'}), 400

            valid_statuses = ['pending', 'in_progress', 'completed']
            if data['status'] not in valid_statuses:
                return jsonify({'error': 'Invalid status. Must be one of: ' + ', '.join(valid_statuses)}), 400

            task.status = data['status']
            task.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Task status updated successfully',
                'task': {
                    'id': task.id,
                    'status': task.status,
                    'updated_at': task.updated_at.isoformat()
                }
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    # Salesman portal APIs
    @app.route('/api/salesman/tasks', methods=['GET'])
    @jwt_required()
    def get_salesman_tasks():
        """Get tasks assigned to the current salesman"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'sub':
                return jsonify({'error': 'Only salesmen can access this endpoint'}), 403

            # Get all tasks assigned to this salesman
            tasks = Task.query.filter_by(salesman_id=current_user.id).order_by(Task.created_at.desc()).all()
            
            # Update task status based on due date
            today = datetime.utcnow().date()
            for task in tasks:
                if task.due_date < today and task.status not in ['completed']:
                    task.status = 'overdue'
            
            db.session.commit()

            return jsonify({
                'tasks': [t.to_dict() for t in tasks]
            }), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/salesman/tasks/<int:task_id>/progress', methods=['PATCH'])
    @jwt_required()
    def update_task_progress(task_id):
        """Update task progress (salesman only)"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'sub':
                return jsonify({'error': 'Only salesmen can update task progress'}), 403

            task = Task.query.get(task_id)
            if not task:
                return jsonify({'error': 'Task not found'}), 404

            if task.salesman_id != current_user.id:
                return jsonify({'error': 'You can only update your own tasks'}), 403

            data = request.get_json() or {}
            current_quantity = data.get('current_quantity')
            
            if current_quantity is None:
                return jsonify({'error': 'current_quantity is required'}), 400

            try:
                current_quantity = int(current_quantity)
                if current_quantity < 0:
                    return jsonify({'error': 'Current quantity cannot be negative'}), 400
                task.current_quantity = current_quantity
                
                # Auto-update status based on progress
                if current_quantity >= task.target_quantity:
                    task.status = 'completed'
                elif current_quantity > 0:
                    task.status = 'in_progress'
                else:
                    task.status = 'pending'
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid current quantity'}), 400

            # Update task status based on due date
            today = datetime.utcnow().date()
            if task.due_date < today and task.status not in ['completed']:
                task.status = 'overdue'

            task.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Task progress updated successfully',
                'task': task.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    # Deals management APIs
    @app.route('/api/deals', methods=['POST'])
    @jwt_required()
    def create_deal():
        """Create a new deal (sub-user only)"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'sub':
                return jsonify({'error': 'Only sub-users can create deals'}), 403

            data = request.get_json() or {}
            
            # Validate required fields
            client_name = (data.get('clientName') or '').strip()
            mobile = (data.get('mobile') or '').strip()
            email = (data.get('email') or '').strip()
            product_name = (data.get('productName') or '').strip()
            price = (data.get('price') or '').strip()
            last_activity_str = data.get('lastActivity')

            if not all([client_name, mobile, email, product_name, price, last_activity_str]):
                return jsonify({'error': 'All fields are required'}), 400

            # Validate email format
            if not validate_email(email):
                return jsonify({'error': 'Invalid email format'}), 400

            # Parse last activity date
            try:
                last_activity = datetime.strptime(last_activity_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

            # Create new deal
            new_deal = Deal(
                client_name=client_name,
                mobile=mobile,
                email=email,
                product_name=product_name,
                price=price,
                last_activity=last_activity,
                salesman_id=current_user.id
            )
            
            db.session.add(new_deal)
            db.session.commit()

            return jsonify({
                'message': 'Deal created successfully',
                'deal': new_deal.to_dict()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/deals', methods=['GET'])
    @jwt_required()
    def list_deals():
        """List deals for the current user"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            if current_user.user_type == 'sub':
                # Sub-user sees their own deals
                deals = Deal.query.filter_by(salesman_id=current_user.id).order_by(Deal.created_at.desc()).all()
            elif current_user.user_type == 'main':
                # Main user sees deals from all their sub-users (both active and inactive)
                sub_user_ids = [u.id for u in current_user.sub_users]
                deals = Deal.query.filter(Deal.salesman_id.in_(sub_user_ids)).order_by(Deal.created_at.desc()).all()
            else:
                return jsonify({'error': 'Invalid user type'}), 400

            return jsonify({
                'deals': [d.to_dict() for d in deals]
            }), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/deals/<int:deal_id>', methods=['PUT'])
    @jwt_required()
    def update_deal(deal_id):
        """Update a deal"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            deal = Deal.query.get(deal_id)
            if not deal:
                return jsonify({'error': 'Deal not found'}), 404

            # Check permissions
            if current_user.user_type == 'sub':
                # Sub-user can only update their own deals
                if deal.salesman_id != current_user.id:
                    return jsonify({'error': 'You can only update your own deals'}), 403
            elif current_user.user_type == 'main':
                # Main user can update deals from their sub-users
                if deal.salesman_id not in [u.id for u in current_user.sub_users if u.is_active]:
                    return jsonify({'error': 'You can only update deals from your salesmen'}), 403
            else:
                return jsonify({'error': 'Invalid user type'}), 403

            data = request.get_json() or {}
            
            # Update fields
            if 'clientName' in data:
                deal.client_name = data['clientName'].strip()
            if 'mobile' in data:
                deal.mobile = data['mobile'].strip()
            if 'email' in data:
                email = data['email'].strip()
                if not validate_email(email):
                    return jsonify({'error': 'Invalid email format'}), 400
                deal.email = email
            if 'productName' in data:
                deal.product_name = data['productName'].strip()
            if 'price' in data:
                deal.price = data['price'].strip()
            if 'lastActivity' in data:
                try:
                    deal.last_activity = datetime.strptime(data['lastActivity'], '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
            if 'status' in data:
                deal.status = data['status']

            deal.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Deal updated successfully',
                'deal': deal.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/deals/<int:deal_id>', methods=['DELETE'])
    @jwt_required()
    def delete_deal(deal_id):
        """Delete a deal"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            deal = Deal.query.get(deal_id)
            if not deal:
                return jsonify({'error': 'Deal not found'}), 404

            # Check permissions
            if current_user.user_type == 'sub':
                # Sub-user can only delete their own deals
                if deal.salesman_id != current_user.id:
                    return jsonify({'error': 'You can only delete your own deals'}), 403
            elif current_user.user_type == 'main':
                # Main user can delete deals from their sub-users
                if deal.salesman_id not in [u.id for u in current_user.sub_users if u.is_active]:
                    return jsonify({'error': 'You can only delete deals from your salesmen'}), 403
            else:
                return jsonify({'error': 'Invalid user type'}), 403

            db.session.delete(deal)
            db.session.commit()

            return jsonify({
                'message': 'Deal deleted successfully'
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/deals/<int:deal_id>/status', methods=['PATCH'])
    @jwt_required()
    def update_deal_status(deal_id):
        """Update deal status (for drag and drop)"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            deal = Deal.query.get(deal_id)
            if not deal:
                return jsonify({'error': 'Deal not found'}), 404

            # Check permissions
            if current_user.user_type == 'sub':
                # Sub-user can only update their own deals
                if deal.salesman_id != current_user.id:
                    return jsonify({'error': 'You can only update your own deals'}), 403
            elif current_user.user_type == 'main':
                # Main user can update deals from their sub-users
                if deal.salesman_id not in [u.id for u in current_user.sub_users if u.is_active]:
                    return jsonify({'error': 'You can only update deals from your salesmen'}), 403
            else:
                return jsonify({'error': 'Invalid user type'}), 403

            data = request.get_json() or {}
            new_status = data.get('status')
            
            if not new_status:
                return jsonify({'error': 'Status is required'}), 400

            # Validate status
            valid_statuses = ['New', 'Qualifying', 'Demo Scheduled', 'Pending Commitment', 'In Negotiation', 'WON', 'LOST']
            if new_status not in valid_statuses:
                return jsonify({'error': 'Invalid status'}), 400

            # Store previous status before updating
            previous_status = deal.status
            deal.previous_status = previous_status
            deal.status = new_status
            deal.updated_at = datetime.utcnow()
            
            # If deal is won or lost, update corresponding lead status
            if new_status in ['WON', 'LOST']:
                # Find leads with matching source_lead_id first, then fallback to name matching
                matching_leads = []
                
                if deal.source_lead_id:
                    # Try to find lead by source_lead_id
                    lead_id = deal.source_lead_id.replace('L', '')  # Remove 'L' prefix
                    try:
                        lead_id_int = int(lead_id)
                        lead = Lead.query.filter_by(id=lead_id_int).first()
                        if lead:
                            matching_leads = [lead]
                    except ValueError:
                        pass
                
                # If no lead found by source_lead_id, fallback to name matching
                if not matching_leads:
                    matching_leads = Lead.query.filter(
                        Lead.salesman_id == deal.salesman_id,
                        Lead.name.ilike(f'%{deal.client_name}%')
                    ).all()
                
                for lead in matching_leads:
                    if new_status == 'WON':
                        lead.status = 'Won'
                    else:  # LOST
                        lead.status = 'Lost'
                    lead.updated_at = datetime.utcnow()
                    print(f"Updated lead {lead.id} ({lead.name}) status to {lead.status} based on deal {deal.id}")
            
            db.session.commit()

            return jsonify({
                'message': 'Deal status updated successfully',
                'deal': deal.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    # Helper function to determine if status change is promotion or demotion
    def get_status_change_type(previous_status, new_status):
        """Determine if a status change is a promotion, demotion, or neutral"""
        status_order = ['New', 'Qualifying', 'Demo Scheduled', 'Pending Commitment', 'In Negotiation', 'WON', 'LOST']
        
        # WON and LOST are final states, any change to them is special
        if new_status in ['WON', 'LOST']:
            return 'completed' if new_status == 'WON' else 'lost'
        
        # If no previous status, it's a new deal
        if not previous_status:
            return 'created'
        
        # If same status, no change
        if previous_status == new_status:
            return 'unchanged'
        
        try:
            prev_index = status_order.index(previous_status)
            new_index = status_order.index(new_status)
            
            if new_index > prev_index:
                return 'promoted'
            elif new_index < prev_index:
                return 'demoted'
            else:
                return 'unchanged'
        except ValueError:
            return 'unchanged'

    # Lead Management APIs
    @app.route('/api/leads', methods=['POST'])
    @jwt_required()
    def create_lead():
        """Create a new lead (sub-user only)"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'sub':
                return jsonify({'error': 'Only sub-users can create leads'}), 403

            data = request.get_json() or {}
            
            # Validate required fields
            name = (data.get('name') or '').strip()
            email = (data.get('email') or '').strip()
            contact_number = (data.get('contactNo') or '').strip()
            product_name = (data.get('productName') or '').strip()
            status = data.get('status', 'New')
            value = data.get('value', 0.0)

            if not all([name, email, contact_number, product_name]):
                return jsonify({'error': 'All fields are required'}), 400

            # Validate email format
            if not validate_email(email):
                return jsonify({'error': 'Invalid email format'}), 400

            # Validate value
            try:
                value = float(value) if value else 0.0
                if value < 0:
                    return jsonify({'error': 'Lead value cannot be negative'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid lead value'}), 400

            # Create new lead (lead_id will be generated in to_dict method)
            new_lead = Lead(
                name=name,
                email=email,
                contact_number=contact_number,
                product_name=product_name,
                status=status,
                value=value,
                salesman_id=current_user.id
            )
            
            db.session.add(new_lead)
            db.session.commit()

            return jsonify({
                'message': 'Lead created successfully',
                'lead': new_lead.to_dict()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/leads', methods=['GET'])
    @jwt_required()
    def list_leads():
        """List leads for the current user"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            if current_user.user_type == 'sub':
                # Sub-user sees their own leads
                leads = Lead.query.filter_by(salesman_id=current_user.id).order_by(Lead.created_at.desc()).all()
            elif current_user.user_type == 'main':
                # Main user sees leads from all their sub-users (both active and inactive)
                sub_user_ids = [u.id for u in current_user.sub_users]
                leads = Lead.query.filter(Lead.salesman_id.in_(sub_user_ids)).order_by(Lead.created_at.desc()).all()
            else:
                return jsonify({'error': 'Invalid user type'}), 400

            # Convert leads to dictionary format safely
            leads_data = []
            for lead in leads:
                try:
                    leads_data.append(lead.to_dict())
                except Exception as e:
                    # If there's an error with a specific lead, skip it but continue
                    print(f"Error converting lead {lead.id} to dict: {e}")
                    continue
            
            return jsonify({
                'leads': leads_data
            }), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/leads/<int:lead_id>', methods=['PUT'])
    @jwt_required()
    def update_lead(lead_id):
        """Update a lead"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            lead = Lead.query.get(lead_id)
            if not lead:
                return jsonify({'error': 'Lead not found'}), 404

            # Check permissions
            if current_user.user_type == 'sub':
                # Sub-user can only update their own leads
                if lead.salesman_id != current_user.id:
                    return jsonify({'error': 'You can only update your own leads'}), 403
            elif current_user.user_type == 'main':
                # Main user can update leads from their sub-users
                if lead.salesman_id not in [u.id for u in current_user.sub_users if u.is_active]:
                    return jsonify({'error': 'You can only update leads from your salesmen'}), 403
            else:
                return jsonify({'error': 'Invalid user type'}), 403

            data = request.get_json() or {}
            
            # Update fields
            if 'name' in data:
                lead.name = data['name'].strip()
            if 'email' in data:
                email = data['email'].strip()
                if not validate_email(email):
                    return jsonify({'error': 'Invalid email format'}), 400
                lead.email = email
            if 'contactNo' in data:
                lead.contact_number = data['contactNo'].strip()
            if 'productName' in data:
                lead.product_name = data['productName'].strip()
            if 'status' in data:
                lead.status = data['status']
            if 'value' in data:
                try:
                    value = float(data['value'])
                    if value < 0:
                        return jsonify({'error': 'Lead value cannot be negative'}), 400
                    lead.value = value
                except (ValueError, TypeError):
                    return jsonify({'error': 'Invalid lead value'}), 400
            if 'lastContact' in data:
                try:
                    lead.last_contact = datetime.strptime(data['lastContact'], '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

            lead.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Lead updated successfully',
                'lead': lead.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/leads/<int:lead_id>', methods=['DELETE'])
    @jwt_required()
    def delete_lead(lead_id):
        """Delete a lead"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            lead = Lead.query.get(lead_id)
            if not lead:
                return jsonify({'error': 'Lead not found'}), 404

            # Check permissions
            if current_user.user_type == 'sub':
                # Sub-user can only delete their own leads
                if lead.salesman_id != current_user.id:
                    return jsonify({'error': 'You can only delete your own leads'}), 403
            elif current_user.user_type == 'main':
                # Main user can delete leads from their sub-users
                if lead.salesman_id not in [u.id for u in current_user.sub_users if u.is_active]:
                    return jsonify({'error': 'You can only delete leads from your salesmen'}), 403
            else:
                return jsonify({'error': 'Invalid user type'}), 403

            db.session.delete(lead)
            db.session.commit()

            return jsonify({
                'message': 'Lead deleted successfully'
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/leads/<int:lead_id>/status', methods=['PATCH'])
    @jwt_required()
    def update_lead_status(lead_id):
        """Update lead status"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            lead = Lead.query.get(lead_id)
            if not lead:
                return jsonify({'error': 'Lead not found'}), 404

            # Check permissions
            if current_user.user_type == 'sub':
                # Sub-user can only update their own leads
                if lead.salesman_id != current_user.id:
                    return jsonify({'error': 'You can only update your own leads'}), 403
            elif current_user.user_type == 'main':
                # Main user can update leads from their sub-users
                if lead.salesman_id not in [u.id for u in current_user.sub_users if u.is_active]:
                    return jsonify({'error': 'You can only update leads from your salesmen'}), 403
            else:
                return jsonify({'error': 'Invalid user type'}), 403

            data = request.get_json() or {}
            new_status = data.get('status')
            
            if not new_status:
                return jsonify({'error': 'Status is required'}), 400

            # Validate status
            valid_statuses = ['New', 'Contacted', 'Qualified', 'Accepted', 'Rejected', 'Won', 'Lost', 'Pipelined']
            if new_status not in valid_statuses:
                return jsonify({'error': 'Invalid status'}), 400

            # If lead is accepted, create a deal in the pipeline and mark as Pipelined
            if new_status == 'Accepted':
                try:
                    # Check if a deal already exists for this lead
                    existing_deal = Deal.query.filter_by(
                        client_name=lead.name,
                        salesman_id=lead.salesman_id,
                        email=lead.email
                    ).first()
                    
                    if not existing_deal:
                        # Create new deal from accepted lead
                        # Format the price properly
                        price_value = lead.value if lead.value and lead.value > 0 else 0
                        formatted_price = f"₹{price_value:,.0f}" if price_value > 0 else "₹0"
                        
                        # Generate lead ID for tracking
                        lead_id = f"L{lead.id:03d}"
                        
                        new_deal = Deal(
                            client_name=lead.name,
                            mobile=lead.contact_number,
                            email=lead.email,
                            product_name=lead.product_name,
                            price=formatted_price,
                            last_activity=datetime.utcnow().date(),
                            status='New',  # Start in the first stage of pipeline
                            salesman_id=lead.salesman_id,
                            source_lead_id=lead_id
                        )
                        db.session.add(new_deal)
                        print(f"Created new deal for accepted lead: {lead.name}")
                        # Mark lead as Pipelined since it's now in the deals pipeline
                        lead.status = 'Pipelined'
                    else:
                        print(f"Deal already exists for lead: {lead.name}")
                        # Mark lead as Pipelined since deal already exists
                        lead.status = 'Pipelined'
                        
                except Exception as e:
                    print(f"Error creating deal for lead {lead.id}: {e}")
                    # If deal creation fails, keep as Accepted
                    lead.status = 'Accepted'
            else:
                # For other statuses (New, Rejected), update normally
                lead.status = new_status
            
            lead.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Lead status updated successfully',
                'lead': lead.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    # Salesman updates API for main users
    @app.route('/api/salesman-updates', methods=['GET'])
    @jwt_required()
    def get_salesman_updates():
        """Get updates from all salesmen for main user"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.user_type != 'main':
                return jsonify({'error': 'Only main users can view salesman updates'}), 403

            # Get all sub-users (both active and inactive)
            sub_users = User.query.filter_by(main_user_id=current_user.id, user_type='sub').all()
            
            updates = []
            for sub_user in sub_users:
                # Get recent deals for this sub-user
                recent_deals = Deal.query.filter_by(salesman_id=sub_user.id).order_by(Deal.updated_at.desc()).limit(5).all()
                
                for deal in recent_deals:
                    # Determine the type of status change
                    change_type = get_status_change_type(deal.previous_status, deal.status)
                    
                    # Create appropriate message based on change type
                    if change_type == 'promoted':
                        title = f'Deal Promoted - {deal.client_name}'
                        content = f'Deal "{deal.product_name}" promoted from {deal.previous_status} to {deal.status}'
                    elif change_type == 'demoted':
                        title = f'Deal Demoted - {deal.client_name}'
                        content = f'Deal "{deal.product_name}" demoted from {deal.previous_status} to {deal.status}'
                    elif change_type == 'completed':
                        title = f'Deal Won - {deal.client_name}'
                        content = f'Deal "{deal.product_name}" successfully closed and won!'
                    elif change_type == 'lost':
                        title = f'Deal Lost - {deal.client_name}'
                        content = f'Deal "{deal.product_name}" was lost'
                    elif change_type == 'created':
                        title = f'New Deal Created - {deal.client_name}'
                        content = f'New deal "{deal.product_name}" created in {deal.status} stage'
                    else:
                        title = f'Deal Update - {deal.client_name}'
                        content = f'Deal "{deal.product_name}" updated to {deal.status} stage'
                    
                    updates.append({
                        'id': f"deal_{deal.id}",
                        'salesman_id': sub_user.id,
                        'salesman_name': f"{sub_user.first_name} {sub_user.last_name}",
                        'date': deal.updated_at.isoformat(),
                        'type': 'deal_update',
                        'change_type': change_type,
                        'title': title,
                        'content': content,
                        'metrics': {
                            'deal_value': deal.price,
                            'client_name': deal.client_name,
                            'current_status': deal.status,
                            'previous_status': deal.previous_status
                        },
                        'status': 'completed' if deal.status in ['WON', 'LOST'] else 'in_progress'
                    })

            # Sort by date (most recent first)
            updates.sort(key=lambda x: x['date'], reverse=True)

            return jsonify({
                'updates': updates,
                'salesmen': [u.to_dict() for u in sub_users]
            }), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    # Meeting Management API endpoints
    @app.route('/api/meetings', methods=['POST'])
    @jwt_required()
    def create_meeting():
        """Create a new meeting"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            data = request.get_json()
            
            # Validate required fields
            required_fields = ['type', 'clientName', 'mobileNumber', 'email', 'date', 'time']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400

            # Validate meeting type specific fields
            if data['type'] == 'offline' and not data.get('venue'):
                return jsonify({'error': 'Venue is required for offline meetings'}), 400
            if data['type'] == 'online' and not data.get('platform'):
                return jsonify({'error': 'Platform is required for online meetings'}), 400

            # Parse date and time
            from datetime import datetime, date, time
            meeting_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            meeting_time = datetime.strptime(data['time'], '%H:%M').time()

            meeting = Meeting(
                type=data['type'],
                client_name=data['clientName'],
                mobile_number=data['mobileNumber'],
                email=data['email'],
                date=meeting_date,
                time=meeting_time,
                venue=data.get('venue'),
                platform=data.get('platform'),
                status=data.get('status', 'Scheduled'),
                salesman_id=current_user.id
            )

            db.session.add(meeting)
            db.session.commit()

            return jsonify({
                'message': 'Meeting created successfully',
                'meeting': meeting.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/meetings', methods=['GET'])
    @jwt_required()
    def get_meetings():
        """Get meetings for the current user"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            if current_user.user_type == 'main':
                # Main user sees meetings from all their sub-users
                sub_user_ids = [u.id for u in current_user.sub_users]
                meetings = Meeting.query.filter(Meeting.salesman_id.in_(sub_user_ids)).order_by(Meeting.date.desc(), Meeting.time.desc()).all()
            else:
                # Sub-user sees only their own meetings
                meetings = Meeting.query.filter_by(salesman_id=current_user.id).order_by(Meeting.date.desc(), Meeting.time.desc()).all()

            return jsonify({
                'meetings': [meeting.to_dict() for meeting in meetings]
            }), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/meetings/<int:meeting_id>', methods=['PUT'])
    @jwt_required()
    def update_meeting(meeting_id):
        """Update a meeting"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            meeting = Meeting.query.get(meeting_id)
            if not meeting:
                return jsonify({'error': 'Meeting not found'}), 404

            # Check permissions
            if current_user.user_type == 'sub':
                if meeting.salesman_id != current_user.id:
                    return jsonify({'error': 'You can only update your own meetings'}), 403
            elif current_user.user_type == 'main':
                # Check if meeting belongs to one of their sub-users
                sub_user_ids = [u.id for u in current_user.sub_users]
                if meeting.salesman_id not in sub_user_ids:
                    return jsonify({'error': 'Meeting not found'}), 404

            data = request.get_json()
            
            # Update fields
            if 'type' in data:
                meeting.type = data['type']
            if 'clientName' in data:
                meeting.client_name = data['clientName']
            if 'mobileNumber' in data:
                meeting.mobile_number = data['mobileNumber']
            if 'email' in data:
                meeting.email = data['email']
            if 'date' in data:
                from datetime import datetime, date
                meeting.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            if 'time' in data:
                from datetime import datetime, time
                meeting.time = datetime.strptime(data['time'], '%H:%M').time()
            if 'venue' in data:
                meeting.venue = data['venue']
            if 'platform' in data:
                meeting.platform = data['platform']
            if 'status' in data:
                meeting.status = data['status']

            meeting.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Meeting updated successfully',
                'meeting': meeting.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/meetings/<int:meeting_id>', methods=['DELETE'])
    @jwt_required()
    def delete_meeting(meeting_id):
        """Delete a meeting"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            meeting = Meeting.query.get(meeting_id)
            if not meeting:
                return jsonify({'error': 'Meeting not found'}), 404

            # Check permissions
            if current_user.user_type == 'sub':
                if meeting.salesman_id != current_user.id:
                    return jsonify({'error': 'You can only delete your own meetings'}), 403
            elif current_user.user_type == 'main':
                # Check if meeting belongs to one of their sub-users
                sub_user_ids = [u.id for u in current_user.sub_users]
                if meeting.salesman_id not in sub_user_ids:
                    return jsonify({'error': 'Meeting not found'}), 404

            db.session.delete(meeting)
            db.session.commit()

            return jsonify({
                'message': 'Meeting deleted successfully'
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.route('/api/meetings/<int:meeting_id>/status', methods=['PATCH'])
    @jwt_required()
    def update_meeting_status(meeting_id):
        """Update meeting status"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            meeting = Meeting.query.get(meeting_id)
            if not meeting:
                return jsonify({'error': 'Meeting not found'}), 404

            # Check permissions
            if current_user.user_type == 'sub':
                if meeting.salesman_id != current_user.id:
                    return jsonify({'error': 'You can only update your own meetings'}), 403
            elif current_user.user_type == 'main':
                # Check if meeting belongs to one of their sub-users
                sub_user_ids = [u.id for u in current_user.sub_users]
                if meeting.salesman_id not in sub_user_ids:
                    return jsonify({'error': 'Meeting not found'}), 404

            data = request.get_json()
            new_status = data.get('status')
            
            if not new_status:
                return jsonify({'error': 'Status is required'}), 400

            # Validate status
            valid_statuses = ['Scheduled', 'Completed', 'Cancelled', 'Postponed']
            if new_status not in valid_statuses:
                return jsonify({'error': 'Invalid status'}), 400

            meeting.status = new_status
            meeting.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Meeting status updated successfully',
                'meeting': meeting.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized'}), 401
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
