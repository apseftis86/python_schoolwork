from config import db, app, bcrypt
from flask import flash, redirect
from sqlalchemy.sql import func
import re


name_validator = re.compile(r'^[a-zA-Z]+$')
password_validator = re.compile(r'^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d)).{8,}$')
email_validator = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User(db.Model):
    __tablename__ = "users"    # optional
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def validate_user(cls, data):
        is_valid = True
        if len(data['first_name']) > 1:
            if not name_validator.match(data['first_name']):
                is_valid = False
                flash('First name can only contain letters', 'error')
        else:
            is_valid = False
            flash('First Name is required', 'error')
        if len(data['last_name']) > 1:
            if not name_validator.match(data['last_name']):
                is_valid = False
                flash('Last name can only contain letters', 'error')
        else:
            is_valid = False
            flash('Last Name is required', 'error')
        if len(data['password']) > 1:
            if data['password'] != data['confirm_password']:
                is_valid = False
                flash('Passwords must match', 'error')
            if not password_validator.match(data['password']):
                is_valid = False
                flash('Password not strong enough', 'error')
        else:
            flash('Password must not be blank', 'error')
            is_valid = False
        if len(data['email']) > 1:
            if not email_validator.match(data['email']):
                flash('Enter valid email address', 'error')
                is_valid = False
        else:
            flash('Email must not be blank', 'error')
            is_valid = False
        return is_valid

    @classmethod
    def register_user(cls, data):
        data = {
            "fn": data['first_name'],
            "ln": data['last_name'],
            "e": data['email'],
            "p": bcrypt.generate_password_hash(data['password']),
        }
        new_user = User(first_name=data['fn'], last_name=data['ln'], email=data['e'], password=data['p'])
        db.session.add(new_user)
        db.session.commit()
        flash('Successfully added!', 'success')
        return new_user

    @classmethod
    def validate_login_data(cls, data):
        is_valid = True
        if len(data['email']) < 1:
            is_valid = False
            flash('Email field blank', 'error')
        if not email_validator.match(data['email']):
            is_valid = False
            flash('Enter valid email address', 'error')
        if len(data['password']) < 1:
            is_valid = False
            flash('Password field blank', 'error')
        return is_valid

    @classmethod
    def login_user(cls, data):
        result = User.query.filter_by(email=data['email']).first()
        if bcrypt.check_password_hash(result.password, data['password']):
            # if we get True after checking the password, we may put the user id in session
            result.last_login = func.now()
            db.session.commit()
            return result
        flash('You could not be logged in', 'error')
        return

