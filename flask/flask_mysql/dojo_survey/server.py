from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import connectToMySQL  # import the function that will return an instance of a connection

app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'  # set a secret key for security purposes

# our index route will handle rendering our form
@app.route('/')
def index():
    mysql = connectToMySQL("users_db")
    locations = mysql.query_db("SELECT * from dojo_locations;")
    mysql2 = connectToMySQL("users_db")
    languages = mysql2.query_db("SELECT * from languages;")
    return render_template('index.html', locations=locations, languages=languages)

@app.route('/submissions')
def submissions():
    mysql = connectToMySQL("users_db")
    users = mysql.query_db('SELECT users.name, users.comment, dojo_locations.name as location, languages.name as language from users '
                                   'LEFT JOIN dojo_locations on dojo_locations.id = users.dojo_location_id '
                                   'LEFT JOIN languages on languages.id = users.language_id;')
    return render_template('submissions.html', users=users)

@app.route('/add', methods=['POST'])
def create_user():
    if len(request.form['name']) < 1:
        flash('Name is required')
    if len(request.form['comment']) > 120:
        flash('Comment cannot be more than 120 characters.')
    if not '_flashes' in session.keys():  # there are no errors
        query = "INSERT into users (name, comment, dojo_location_id, language_id, created_at) VALUES (%(n)s, %(c)s, %(dl)s, %(l)s, now())"
        data = {
            "n": request.form['name'],
            "c": request.form['comment'],
            "dl": request.form['dojo_location_id'],
            "l": request.form['language_id'],
        }
        user_added = connectToMySQL('users_db').query_db(query, data)
        get_user = connectToMySQL('users_db').query_db('SELECT users.name, users.comment, dojo_locations.name as location, languages.name as language from users '
                                   'LEFT JOIN dojo_locations on dojo_locations.id = users.dojo_location_id '
                                   'LEFT JOIN languages on languages.id = users.language_id WHERE users.id = {};'.format(user_added))
        session['user'] = get_user[0]
        return redirect('/result')
    else:
        return redirect('/')

@app.route('/result')
def result_submitted():
    user = session['user']
    return render_template('result.html', user=user)


if __name__ == "__main__":
    app.run(debug=True)