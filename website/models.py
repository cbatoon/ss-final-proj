# stores database models

from . import db
from flask_login import UserMixin
from datetime import datetime

# UserMixin implements authentication methods

class User(db.Model, UserMixin): # roles: employee, admin, owner
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    role = db.Column(db.String(20), nullable=False, default="employee")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Customer(db.Model):
    customerNum = db.Column(db.Integer, primary_key=True, nullable=False)
    customerFirst = db.Column(db.String(150))     
    customerLast = db.Column(db.String(150))        
    address = db.Column(db.String(20))            
    balance = db.Column(db.Float)                    
    creditScore = db.Column(db.Integer)            
    bankNumR = db.Column(db.Integer)              
    bankNumA = db.Column(db.String(12))           
    SSN = db.Column(db.Integer)               

class AuditLogging(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # specific user did what
    action = db.Column(db.String(100), nullable=False)          # tracks actions
    details = db.Column(db.Text)                                # additional info 
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) # when action happened
    user = db.relationship('User', backref='logs')