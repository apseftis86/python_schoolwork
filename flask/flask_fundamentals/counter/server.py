from flask import Flask, render_template, request, redirect, session
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes

@app.route('/')
def session_counter():
    if 'counter' in session:
        session['visit_counter'] += 1
        session['counter'] += 1
    else:
        session['visit_counter'] += 1
        session['counter'] = 1
    return render_template('index.html', counter=session['counter'], visits=session['visit_counter'])

@app.route('/update_two')
def add_two():
    session['counter'] += 1
    return redirect('/')

@app.route('/destroy_session')
def destroying_session():
    session.pop('counter')
    return redirect('/')

@app.route('/custom_increments', methods=['POST'])
def custom_inc():
    increment_by = int(request.form['increments'])
    session['counter'] += increment_by - 1
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)