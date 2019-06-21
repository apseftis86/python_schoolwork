from flask import Flask, render_template, request, redirect, flash, session
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL  # import the function that will return an instance of a connection
import re
from datetime import date, datetime, timedelta

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
        mysql.query_db(query, data)
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
        if result:
            if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
                # if we get True after checking the password, we may put the user id in session
                if not result[0]['last_login']:
                    session['first_login'] = True
                # update last login time
                update_login_time = connectToMySQL('dojo_tweets')
                update_login_time.query_db(f"UPDATE users set last_login = now() where id = {result[0]['id']};")
                session['userid'] = result[0]['id']
                session['user'] = result[0]
                # never render on a post, always redirect!
                return redirect('/dashboard')
        flash('You could not be logged in', 'error')
        return redirect('/')
    return redirect('/')


@app.route('/dashboard')
def success():
    if 'userid' not in session:
        return redirect('/')
    tweet_mysql = connectToMySQL('dojo_tweets')
    liked_tweets = connectToMySQL('dojo_tweets')
    my_liked_tweets = liked_tweets.query_db(f"SELECT * from tweet_likes where liked_user_id = {session['userid']}")


    tweets = tweet_mysql.query_db(f"SELECT tweets.content as content, tweets.id, tweets.user_id as user_id, tweets.created_at as created_at, tweets.updated_at as updated_at "
                                  f", count(tweet_likes.id) as likes, users.first_name as first_name, users.last_name as last_name from tweets "
                                  f"LEFT join tweet_likes on tweet_likes.tweet_id = tweets.id "
                                  f"LEFT JOIN following on following.following_user_id = tweets.user_id "
                                  f"LEFT join users on users.id = tweets.user_id "
                                  f"WHERE following.primary_user_id = {session['userid']} or tweets.user_id = {session['userid']} GROUP BY (tweets.id);")
    follow_count_mysql = connectToMySQL('dojo_tweets')
    follow_count = follow_count_mysql.query_db(f"SELECT count(following_user_id) from following where primary_user_id = {session['userid']} group by following_user_id")
    if not follow_count:
        session['not_following'] = True
    for tweet in tweets:
        created = tweet['created_at']
        viewed = datetime.now()
        delta = viewed - created
        if delta.days < 1:
            if int(delta.seconds/60/60) > 1:
                tweet['since_created'] = str(int(delta.seconds/60/60)) + ' hours'
            elif int(delta.seconds/60/60)== 1:
                tweet['since_created'] = str(int(delta.seconds/60/60)) + ' hour'
            else:
                tweet['since_created'] = str(int(delta.seconds / 60 )) + ' minutes'
        else:
            if delta.days == 1:
                tweet['since_created'] = str(delta.days) + ' day'
            else:
                tweet['since_created'] = str(delta.days) + ' days'
        print(tweet['created_at'])
        for my_liked in my_liked_tweets:
            if tweet['id'] == my_liked['tweet_id']:
                tweet['liked_by_me'] = True
        if tweet['user_id'] == session['userid']:
            tweet['owned_by_me'] = True
    return render_template('dashboard.html', user=session['user'], tweets=tweets)


@app.route('/tweet/create', methods=['POST'])
def create_tweet():
    if 'userid' not in session:
        return redirect('/')
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
    if 'userid' not in session:
        return redirect('/')
    mysql = connectToMySQL('dojo_tweets')
    query = f"DELETE from tweets where id = {id} and user_id = {session['userid']};"
    mysql.query_db(query)
    return redirect('/dashboard')


@app.route('/tweet/<id>/like')
def like_tweet(id):
    if 'userid' not in session:
        return redirect('/')
    check = connectToMySQL('dojo_tweets')
    tweet_liked = check.query_db(f"SELECT * from tweet_likes where tweet_id = {id} and liked_user_id = {session['userid']}")
    if not tweet_liked:
        mysql = connectToMySQL('dojo_tweets')
        query = f"INSERT into tweet_likes (tweet_id, liked_user_id, created_at, updated_at) values ({id}, {session['userid']}, now(), now());"
        mysql.query_db(query)
    return redirect('/dashboard')


@app.route('/tweet/<id>/edit')
def edit_tweet(id):
    if 'userid' not in session:
        return redirect('/')
    edit_tweet = connectToMySQL('dojo_tweets')
    tweet = edit_tweet.query_db(f"SELECT * from tweets where id = {id} and user_id = {session['userid']}")
    if tweet:
        return render_template('edit.html', tweet=tweet[0])
    return render_template('edit.html', tweet=None)

@app.route('/tweet/<id>/update', methods=['POST'])
def update_tweet(id):
    if 'userid' not in session:
        return redirect('/')
    if len(request.form['content']) < 1:
        flash('Tweet length cannot be 0', 'error')
    elif len(request.form['content']) > 255:
        flash('Tweet cannot be longer than 255 characters', 'error')
    if not '_flashes' in session.keys():
        if request.form['button'] == 'Update':
            update_tweet_mysql = connectToMySQL('dojo_tweets')
            query = f"UPDATE tweets SET content = %(c)s, updated_at = now() WHERE id = {id};"
            data = {
                "c": request.form['content']
            }
            update_tweet = update_tweet_mysql.query_db(query, data)
            return redirect('/dashboard')
        else:
            return redirect('/dashboard')
    return redirect(f'/tweet/{id}/edit')


@app.route('/tweet/<id>/unlike')
def unlike_tweet(id):
    if 'userid' not in session:
        return redirect('/')
    check = connectToMySQL('dojo_tweets')
    tweet_liked = check.query_db(f"SELECT * from tweet_likes where tweet_id = {id} and liked_user_id = {session['userid']}")
    if tweet_liked:
        mysql = connectToMySQL('dojo_tweets')
        query = f"DELETE from tweet_likes where id = {tweet_liked[0]['id']};"
        mysql.query_db(query)
    return redirect('/dashboard')

@app.route('/users')
def choices():
    if 'userid' not in session:
        return redirect('/')
    users_mysql = connectToMySQL('dojo_tweets')
    users = users_mysql.query_db(f"SELECT users.id, users.first_name, users.last_name, users.email from users where users.id != {session['userid']};")
    for user in users:
        check_followed_by = connectToMySQL('dojo_tweets')
        followed_by = check_followed_by.query_db(f"SELECT * from following where primary_user_id = {session['userid']} and following_user_id = {user['id']};")
        if followed_by:
            user['followed_by_me'] = True
    return render_template('users.html', users=users)


@app.route('/users/<id>/unfollow')
def unfollow_user(id):
    if 'userid' not in session:
        return redirect('/')
    query = f"DELETE FROM following where primary_user_id = {session['userid']} and following_user_id = {id};"
    unfollow = connectToMySQL('dojo_tweets')
    unfollow.query_db(query)
    return redirect('/users')


@app.route('/users/<id>/follow')
def follow_user(id):
    if 'userid' not in session:
        return redirect('/')
    query = f"INSERT INTO following (primary_user_id, following_user_id) VALUES ({session['userid']}, {id});"
    follow = connectToMySQL('dojo_tweets')
    follow.query_db(query)
    return redirect('/users')


@app.route('/add', methods=['POST'])
def add():
    if 'userid' not in session:
        return redirect('/login')
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