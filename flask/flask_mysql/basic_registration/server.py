from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import connectToMySQL  # import the function that will return an instance of a connection

app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'  # set a secret key for security purposes

# our index route will handle rendering our form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_user():
    if len(request.form['first_name']) < 1:
        flash('First Name is required')
    if len(request.form['last_name']) < 1:
        flash('Last Name is required')
    if request.form['password'] != request.form['confirm_password']:
        flash('Passwords must match')
    if not '_flashes' in session.keys():  # there are no errors
        query = "INSERT into users (first_name, last_name, password, created_at) VALUES (%(fn)s, %(ln)s, %(p)s, now())"
        data = {
            "fn": request.form['first_name'],
            "ln": request.form['comment'],
            "p": request.form['dojo_location_id'],
        }
        user_added = connectToMySQL('users_db').query_db(query, data)
        flash('Thank you for your submission')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)