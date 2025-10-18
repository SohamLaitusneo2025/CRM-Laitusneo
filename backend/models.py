from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    # New fields for sub-user support
    username = db.Column(db.String(50), unique=True, nullable=True, index=True)
    contact_number = db.Column(db.String(20), nullable=True)
    user_type = db.Column(db.Enum('main', 'sub'), nullable=False, default='main')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # For sub users - reference to main user
    main_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relationship for sub users
    sub_users = db.relationship('User', backref=db.backref('main_user', remote_side=[id]))

    def __init__(self, email, password, first_name, last_name, user_type='main', main_user_id=None, username=None, contact_number=None):
        self.email = email
        self.password_hash = self.hash_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.user_type = user_type
        self.main_user_id = main_user_id
        self.username = username
        self.contact_number = contact_number

    def hash_password(self, password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def check_password(self, password):
        """Check if provided password matches the hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'contact_number': self.contact_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_type': self.user_type,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'main_user_id': self.main_user_id
        }
    
    def __repr__(self):
        return f'<User {self.email}>'


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.String(50))
    delivery_timeline = db.Column(db.String(100))
    technologies = db.Column(db.String(200))
    github_link = db.Column(db.String(200))
    preview_link = db.Column(db.String(200))
    ppt_link = db.Column(db.String(200))
    demo_video_link = db.Column(db.String(200))
    admin_name = db.Column(db.String(100))
    conversation_flow_link = db.Column(db.String(200))
    status = db.Column(db.Enum('working', 'under_maintenance', 'rejected'), default='working')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign key to main user
    main_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship to user
    user = db.relationship('User', backref=db.backref('products', lazy=True))
    
    def to_dict(self):
        """Convert product object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'delivery_timeline': self.delivery_timeline,
            'technologies': self.technologies,
            'github_link': self.github_link,
            'preview_link': self.preview_link,
            'ppt_link': self.ppt_link,
            'demo_video_link': self.demo_video_link,
            'admin_name': self.admin_name,
            'conversation_flow_link': self.conversation_flow_link,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'main_user_id': self.main_user_id
        }
    
    def __repr__(self):
        return f'<Product {self.name}>'


class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(20), unique=True, nullable=False)  # T001, T002, etc.
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    target_quantity = db.Column(db.Integer, default=0)
    current_quantity = db.Column(db.Integer, default=0)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Enum('low', 'medium', 'high'), default='medium')
    status = db.Column(db.Enum('pending', 'in_progress', 'completed', 'overdue'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign keys
    salesman_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    assigned_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    salesman = db.relationship('User', foreign_keys=[salesman_id], backref=db.backref('assigned_tasks', lazy=True))
    product = db.relationship('Product', backref=db.backref('tasks', lazy=True))
    assigned_by = db.relationship('User', foreign_keys=[assigned_by_id], backref=db.backref('created_tasks', lazy=True))
    
    def to_dict(self):
        """Convert task object to dictionary"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'target_quantity': self.target_quantity,
            'current_quantity': self.current_quantity,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'salesman_id': self.salesman_id,
            'product_id': self.product_id,
            'assigned_by_id': self.assigned_by_id,
            'salesman_name': f"{self.salesman.first_name} {self.salesman.last_name}" if self.salesman else None,
            'product_name': self.product.name if self.product else None
        }
    
    def __repr__(self):
        return f'<Task {self.task_id}: {self.title}>'


class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    # lead_id column - only add if it exists in the database
    # We'll handle this dynamically in the to_dict method
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Enum('New', 'Contacted', 'Qualified', 'Accepted', 'Rejected', 'Won', 'Lost', 'Pipelined'), default='New')
    value = db.Column(db.Float, default=0.0)
    last_contact = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign key to sub-user (salesman) who created the lead
    salesman_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship to user
    salesman = db.relationship('User', backref=db.backref('leads', lazy=True))
    
    def __init__(self, **kwargs):
        # Remove lead_id from kwargs if it doesn't exist in the database
        if 'lead_id' in kwargs:
            # Check if lead_id column exists by trying to access it
            try:
                # This will fail if the column doesn't exist
                super().__init__(**kwargs)
            except Exception:
                # Remove lead_id and try again
                kwargs.pop('lead_id', None)
                super().__init__(**kwargs)
        else:
            super().__init__(**kwargs)
    
    def to_dict(self):
        """Convert lead object to dictionary"""
        # Generate lead_id using the id since lead_id column doesn't exist
        display_lead_id = f"L{self.id:03d}"
        
        return {
            'id': self.id,
            'lead_id': display_lead_id,
            'name': self.name,
            'email': self.email,
            'contactNo': self.contact_number,
            'productName': self.product_name,
            'status': self.status,
            'value': self.value,
            'lastContact': self.last_contact.isoformat() if self.last_contact else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'salesman_id': self.salesman_id,
            'salesman_name': f"{self.salesman.first_name} {self.salesman.last_name}" if self.salesman else None
        }
    
    def __repr__(self):
        return f'<Lead {self.id}: {self.name} - {self.product_name}>'


class Deal(db.Model):
    __tablename__ = 'deals'
    
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    last_activity = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('New', 'Qualifying', 'Demo Scheduled', 'Pending Commitment', 'In Negotiation', 'WON', 'LOST'), default='New')
    previous_status = db.Column(db.Enum('New', 'Qualifying', 'Demo Scheduled', 'Pending Commitment', 'In Negotiation', 'WON', 'LOST'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign key to sub-user (salesman)
    salesman_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Track source lead ID
    source_lead_id = db.Column(db.String(20), nullable=True)
    
    # Relationship to user
    salesman = db.relationship('User', backref=db.backref('deals', lazy=True))
    
    def to_dict(self):
        """Convert deal object to dictionary"""
        # Check if this deal was created from a lead
        fromLead = bool(self.source_lead_id)
        leadId = self.source_lead_id
            
        return {
            'id': self.id,
            'clientName': self.client_name,
            'mobile': self.mobile,
            'email': self.email,
            'productName': self.product_name,
            'price': self.price,
            'lastActivity': self.last_activity.isoformat() if self.last_activity else None,
            'status': self.status,
            'previous_status': self.previous_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'salesman_id': self.salesman_id,
            'salesman_name': f"{self.salesman.first_name} {self.salesman.last_name}" if self.salesman else None,
            'fromLead': fromLead,
            'leadId': leadId
        }
    
    def __repr__(self):
        return f'<Deal {self.id}: {self.client_name} - {self.product_name}>'


class Meeting(db.Model):
    __tablename__ = 'meetings'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum('offline', 'online', 'google-meet'), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    product_name = db.Column(db.String(200), nullable=True)
    venue = db.Column(db.String(200), nullable=True)
    platform = db.Column(db.String(50), nullable=True)
    meeting_link = db.Column(db.String(500), nullable=True)  # For online meetings
    google_maps_link = db.Column(db.String(500), nullable=True)  # For offline meetings
    message = db.Column(db.Text, nullable=True)  # Personal message for client
    status = db.Column(db.Enum('Scheduled', 'Completed', 'Cancelled', 'Postponed'), default='Scheduled', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign key to the user who created the meeting
    salesman_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    salesman = db.relationship('User', backref='meetings')
    product = db.relationship('Product', backref='meetings')

    def __init__(self, type, client_name, mobile_number, email, date, time, product_id=None, product_name=None, venue=None, platform=None, meeting_link=None, google_maps_link=None, message=None, status='Scheduled', salesman_id=None):
        self.type = type
        self.client_name = client_name
        self.mobile_number = mobile_number
        self.email = email
        self.date = date
        self.time = time
        self.product_id = product_id
        self.product_name = product_name
        self.venue = venue
        self.platform = platform
        self.meeting_link = meeting_link
        self.google_maps_link = google_maps_link
        self.message = message
        self.status = status
        self.salesman_id = salesman_id

    def to_dict(self):
        """Convert meeting object to dictionary"""
        return {
            'id': self.id,
            'type': self.type,
            'clientName': self.client_name,
            'mobileNumber': self.mobile_number,
            'email': self.email,
            'date': self.date.isoformat() if self.date else None,
            'time': self.time.strftime('%H:%M') if self.time else None,
            'productId': self.product_id,
            'productName': self.product_name,
            'venue': self.venue,
            'platform': self.platform,
            'meetingLink': self.meeting_link,
            'googleMapsLink': self.google_maps_link,
            'message': self.message,
            'status': self.status,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'salesman_id': self.salesman_id,
            'salesman_name': f"{self.salesman.first_name} {self.salesman.last_name}" if self.salesman else None
        }
    
    def __repr__(self):
        return f'<Meeting {self.id}: {self.client_name} - {self.date} {self.time}>'


class Campaign(db.Model):
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_name = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(300), nullable=False)
    email_body = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('Draft', 'Sending', 'Sent', 'Failed'), default='Draft', nullable=False)
    total_recipients = db.Column(db.Integer, default=0)
    sent_count = db.Column(db.Integer, default=0)
    failed_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign key to sub-user who created the campaign
    salesman_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship to user
    salesman = db.relationship('User', backref=db.backref('campaigns', lazy=True))
    
    def to_dict(self):
        """Convert campaign object to dictionary"""
        # Generate campaign_id like C001, C002, etc.
        campaign_id = f"C{self.id:03d}"
        
        return {
            'id': self.id,
            'campaignId': campaign_id,
            'campaignName': self.campaign_name,
            'subject': self.subject,
            'emailBody': self.email_body,
            'status': self.status,
            'totalRecipients': self.total_recipients,
            'sentCount': self.sent_count,
            'failedCount': self.failed_count,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'sentAt': self.sent_at.isoformat() if self.sent_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'salesman_id': self.salesman_id,
            'salesman_name': f"{self.salesman.first_name} {self.salesman.last_name}" if self.salesman else None
        }
    
    def __repr__(self):
        return f'<Campaign {self.id}: {self.campaign_name}>'


class CampaignEmail(db.Model):
    __tablename__ = 'campaign_emails'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    recipient_email = db.Column(db.String(120), nullable=False)
    recipient_name = db.Column(db.String(100), nullable=True)
    status = db.Column(db.Enum('Pending', 'Sent', 'Failed', 'Bounced'), default='Pending', nullable=False)
    error_message = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)
    opened_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship to campaign
    campaign = db.relationship('Campaign', backref=db.backref('emails', lazy=True, cascade='all, delete-orphan'))
    
    def to_dict(self):
        """Convert campaign email object to dictionary"""
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'recipientEmail': self.recipient_email,
            'recipientName': self.recipient_name,
            'status': self.status,
            'errorMessage': self.error_message,
            'sentAt': self.sent_at.isoformat() if self.sent_at else None,
            'openedAt': self.opened_at.isoformat() if self.opened_at else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<CampaignEmail {self.id}: {self.recipient_email}>'
