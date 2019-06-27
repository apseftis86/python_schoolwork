from flask import render_template, request, redirect, flash, session
from datetime import date, datetime, timedelta
from models import User

def index():
    if 'userid' in session:
        return redirect('/dashboard')
    return render_template('login.html')

def register():
    validated_data = User.validate_user(request.form)
    if validated_data:
        User.register_user(request.form)
        return redirect('/')
    return redirect('/')

def login():
    validated_data = User.validate_login_data(request.form)
    if validated_data:
        result = User.login_user(request.form)
        session['userid'] = result.id
        return redirect('/dashboard')
    return redirect('/')

def dashboard():
    if 'userid' not in session:
        return redirect('/')
    user = User.query.get(int(session['userid']))
    return render_template('dashboard.html', user=user)

def logout():
    session.clear()
    return redirect('/')

