from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

class user(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100),nullable = False)
    password = db.Column(db.String(100),nullable = False)
    user_sts = db.Column(db.Boolean, default = False, nullable = False)

class Req_donner_details(db.Model):
    __tablename__ = 'req_donner_details'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Phone = db.Column(db.String(15), nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    Address = db.Column(db.String(100), nullable=False)
    State = db.Column(db.String(50), nullable=False)
    District = db.Column(db.String(50), nullable=False)
    BloodGroup = db.Column(db.String(10), nullable=False)
    Message = db.Column(db.String(100), nullable=False)
    
class Active_donner_details(db.Model):
    __tablename__ = 'active_donner_details'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Phone = db.Column(db.String(15), nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    Address = db.Column(db.String(100), nullable=False)
    State = db.Column(db.String(50), nullable=False)
    District = db.Column(db.String(50), nullable=False)
    BloodGroup = db.Column(db.String(10), nullable=False)
    Message = db.Column(db.String(100), nullable=False)

class fund_donation(db.Model):
    __tablename__ = 'fund_donation'
    Name = db.Column(db.String(50), primary_key=True, nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Donation_amount = db.Column(db.Integer, nullable=False)
    Message = db.Column(db.String(100), nullable=False)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50),nullable = False)
    Type = db.Column(db.String(50), nullable = False)
    Commends = db.Column(db.String(1000),nullable =False )