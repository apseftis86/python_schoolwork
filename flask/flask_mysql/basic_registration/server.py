from flask import Flask, render_template, request, redirect, flash, session
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL  # import the function that will return an instance of a connection
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'keep it secret, keep it safe'  # set a secret key for security purposes

# our index route will handle rendering our form
name_validator = re.compile(r'^[a-zA-Z]+$')
password_validator = re.compile(r'^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d)).{8,}$')
email_validator = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
@app.route('/')
def index():
    if 'userid' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def success():
    if 'userid' not in session:
        return redirect('/')
    user_mysql = connectToMySQL('dojo_tweets')
    tweet_mysql = connectToMySQL('dojo_tweets')
    follower_mysql = connectToMySQL('dojo_tweets')
    user = user_mysql.query_db(f"SELECT first_name,last_name, email, "
                               f"last_login from users where id = {session['userid']}")
    print(user[0])
    following_tweets = follower_mysql.query_db(f"SELECT tweets.id as id, tweets.content as content, tweets.created_at as created_at, tweets.updated_at as updated_at, "
                                               f"count(tweet_likes.id) as likes, users.first_name as first_name, users.last_name as last_name from tweets "
                                               f"LEFT JOIN tweet_likes on tweet_likes.tweet_id = tweets.id "
                                        f"LEFT JOIN following on following.following_user_id = tweets.user_id "
                                        f"LEFT JOIN users on users.id = following.following_user_id where following.primary_user_id = {session['userid']} GROUP by (tweets.id)")
    liked_tweets = connectToMySQL('dojo_tweets')
    my_liked_tweets = liked_tweets.query_db(f"SELECT * from tweet_likes where liked_user_id = {session['userid']}")
    user_tweets = tweet_mysql.query_db(f"SELECT * from tweets where user_id = {session['userid']}")
    print(my_liked_tweets)
    for tweet in following_tweets:
        for my_liked in my_liked_tweets:
            if tweet['id'] == my_liked['tweet_id']:
                tweet['liked_by_me'] = True
    return render_template('dashboard.html', user=user[0], tweets=user_tweets, following_tweets=following_tweets)

@app.route('/register', methods=['POST'])
def register_user():
    mysql = connectToMySQL('dojo_tweets')
    if len(request.form['first_name']) > 1:
        if not name_validator.match(request.form['first_name']):
            flash('First name can only contain letters', 'error')
    else:
        flash('First Name is required', 'error')
    if len(request.form['last_name']) > 1:
        if not name_validator.match(request.form['last_name']):
            flash('Last name can only contain letters', 'error')
    else:
        flash('Last Name is required', 'error')
    if len(request.form['password']) > 1:
        if request.form['password'] != request.form['confirm_password']:
            flash('Passwords must match', 'error')
        if not password_validator.match(request.form['password']):
            flash('Password not strong enough', 'error')
    else:
        flash('Password must not be blank', 'error')
    if len(request.form['email']) > 1:
        if not email_validator.match(request.form['email']):
            flash('Enter valid email address', 'error')
    else:
        flash('Email must not be blank', 'error')
    if not '_flashes' in session.keys():  # there are no errors
        query = "INSERT into users (first_name, last_name, email, password, created_at) VALUES (%(fn)s, %(ln)s, %(e)s, %(p)s, now());"
        data = {
            "fn": request.form['first_name'],
            "ln": request.form['last_name'],
            "e": request.form['email'],
            "p": bcrypt.generate_password_hash(request.form['password']),
        }
        user_added = mysql.query_db(query, data)
        flash('Successfully added!', 'success')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    if len(request.form['email']) < 1:
        flash('Email field blank', 'error')
    if not email_validator.match(request.form['email']):
        flash('Enter valid email address', 'error')
    if len(request.form['password']) < 1:
        flash('Password field blank', 'error')
    if not '_flashes' in session.keys():
        mysql = connectToMySQL('dojo_tweets')
        query = "SELECT * FROM users where email = %(e)s"
        data = {
            "e": request.form['email']
        }
        result = mysql.query_db(query, data)
        print(result)
        if result:
            if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
                # if we get True after checking the password, we may put the user id in session
                if not result[0]['last_login']:
                    session['first_login'] = True
                # update last login time
                update_login_time = connectToMySQL('dojo_tweets')
                update_login_time.query_db(f"UPDATE users set last_login = now() where id = {result[0]['id']};")
                session['userid'] = result[0]['id']
                # never render on a post, always redirect!
                return redirect('/dashboard')
        flash('You could not be logged in', 'error')
        return redirect('/')
    return redirect('/')

@app.route('/tweet/create', methods=['POST'])
def create_tweet():
    if len(request.form['content']) > 255:
        flash('Tweet cannot be more than 255 characters', 'error')
    if len(request.form['content']) < 1:
        flash('Tweet cannot be empty', 'error')
    if not '_flashes' in session.keys():
        if 'userid' in session:
            query = f"INSERT into tweets (content, user_id, created_at) VALUES (%(c)s, {session['userid']}, now());"
            data = {
                "c": request.form['content'],
            }
            mysql = connectToMySQL('dojo_tweets')
            tweet_added = mysql.query_db(query, data)
        return redirect('/dashboard')
    return redirect('/dashboard')

@app.route('/tweet/<id>/delete')
def delete_tweet(id):
    mysql = connectToMySQL('dojo_tweets')
    query = f"DELETE from tweets where id = {id} and user_id = {session['userid']};"
    mysql.query_db(query)
    return redirect('/dashboard')

@app.route('/tweet/<id>/like')
def like_tweet(id):
    check = connectToMySQL('dojo_tweets')
    tweet_liked = check.query_db(f"SELECT * from tweet_likes where tweet_id = {id} and liked_user_id = {session['userid']}")
    if not tweet_liked:
        mysql = connectToMySQL('dojo_tweets')
        query = f"INSERT into tweet_likes (tweet_id, liked_user_id, created_at, updated_at) values ({id}, {session['userid']}, now(), now());"
        mysql.query_db(query)
    return redirect('/dashboard')

@app.route('/tweet/<id>/unlike')
def unlike_tweet(id):
    check = connectToMySQL('dojo_tweets')
    tweet_liked = check.query_db(f"SELECT * from tweet_likes where tweet_id = {id} and liked_user_id = {session['userid']}")
    print(tweet_liked)
    if tweet_liked:
        mysql = connectToMySQL('dojo_tweets')
        query = f"DELETE from tweet_likes where id = {tweet_liked[0]['id']};"
        mysql.query_db(query)
    return redirect('/dashboard')

@app.route('/add-friends')
def choices():
    follow_choices = []
    not_followed = []
    followed = []
    users_mysql = connectToMySQL('dojo_tweets')
    users = users_mysql.query_db(f"SELECT users.id, users.first_name, users.last_name, following.primary_user_id as followed_by from users "
                                 f"LEFT JOIN following on users.id = following.following_user_id "
                                 f"where users.id != {session['userid']};")
    for user in users:
        if user['followed_by'] != session['userid']:
            follow_choices.append(user)
        else:
            followed.append(user['id'])
    for choice in follow_choices:
        if choice['id'] not in followed:
            not_followed.append(choice)
    print(not_followed)
    return render_template('add.html', users=not_followed)

@app.route('/add', methods=['POST'])
def add():
    users = request.form.getlist('follow[]')
    for user in users:
        users_mysql = connectToMySQL('dojo_tweets')
        users_mysql.query_db(f"INSERT INTO following (primary_user_id, following_user_id) VALUES ({session['userid']}, {user})")
    return redirect('/add-friends')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)