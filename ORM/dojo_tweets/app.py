from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date, datetime, timedelta
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import func                         # ADDED THIS LINE FOR DEFAULT TIMESTAMP
from werkzeug.utils import secure_filename
import os
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)

UPLOAD_FOLDER = 'static/img/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# configurations to tell our app about the database we'll be connecting to
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dojo_tweets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# a tool for allowing migrations/creation of tables
migrate = Migrate(app, db)
app.secret_key = 'keep it secret, keep it safe'  # set a secret key for security purposes

# our index route will handle rendering our form
name_validator = re.compile(r'^[a-zA-Z]+$')
# password_validator = re.compile(r'^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d)).{8,}$')
email_validator = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
likes_table = db.Table('likes',
              db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
              db.Column('tweet_id', db.Integer, db.ForeignKey('tweets.id'), primary_key=True))

followers_table =  db.Table('followers',
              db.Column('follower_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
              db.Column('following_id', db.Integer, db.ForeignKey('users.id'), primary_key=True))

class User(db.Model):
    __tablename__ = "users"    # optional
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(100))
    last_login = db.Column(db.DateTime(timezone=True), default=func.now())
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    tweets_this_user_likes = db.relationship('Tweet', secondary=likes_table)
    users_this_person_follows = db.relationship('User',
        secondary = followers_table,
        primaryjoin = (followers_table.c.follower_id == id),
        secondaryjoin = (followers_table.c.following_id == id),
        backref = db.backref('followers', lazy = 'dynamic'),
        lazy = 'dynamic')

    def followed_tweets(self):
        followed = Tweet.query.join(
            followers_table, (followers_table.c.following_id == Tweet.user_id)).filter(
            followers_table.c.follower_id == self.id)
        own = Tweet.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Tweet.created_at.desc())

class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    viewed_at = db.Column(db.DateTime(timezone=True), default=func.now())    # notice the extra import statement above
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_info = db.relationship('User', foreign_keys=[user_id], backref="user_tweets")
    users_who_like_this_tweet = db.relationship('User', secondary=likes_table)

class Avatar(db.Model):
    __tablename__ = "avatars"
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(45))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_info = db.relationship('User', foreign_keys=[user_id], backref="user_avatar")
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())

@app.route('/')
def index():
    if 'userid' in session:
        return redirect('/dashboard')
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register_user():
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
        # if not password_validator.match(request.form['password']):
            # flash('Password not strong enough', 'error')
    else:
        flash('Password must not be blank', 'error')
    if len(request.form['email']) > 1:
        if not email_validator.match(request.form['email']):
            flash('Enter valid email address', 'error')
    else:
        flash('Email must not be blank', 'error')
    if not '_flashes' in session.keys():  # there are no errors
        data = {
            "fn": request.form['first_name'],
            "ln": request.form['last_name'],
            "e": request.form['email'],
            "p": bcrypt.generate_password_hash(request.form['password']),
        }
        new_user = User(first_name=data['fn'], last_name=data['ln'], email=data['e'], password=data['p'])
        db.session.add(new_user)
        db.session.commit()
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
        result = User.query.filter_by(email=request.form['email']).first()
        if bcrypt.check_password_hash(result.password, request.form['password']):
            # if we get True after checking the password, we may put the user id in session
            result.last_login = func.now()
            db.session.commit()
            session['userid'] = result.id
            session['user'] = {
                'first_name': result.first_name,
                'last_name': result.last_name,
                'email': result.email,
                'last_login': result.last_login - timedelta(hours=4),
            }
            # never render on a post, always redirect!
            return redirect('/dashboard')
        flash('You could not be logged in', 'error')
        return redirect('/')
    return redirect('/')


@app.route('/dashboard')
def success():
    if 'userid' not in session:
        return redirect('/')
    user = User.query.get(int(session['userid']))
    tweets = user.followed_tweets().all()
    following = 0
    for follow_user in user.users_this_person_follows:
        following += 1
    if following == 0:
        user.none_following = True
    for tweet in tweets:
        tweet.likes = len(tweet.users_who_like_this_tweet)
        created = tweet.created_at - timedelta(hours=4)
        viewed = datetime.now()
        delta = viewed - created
        if delta.days < 1:
            if int(delta.seconds/60/60) > 1:
                tweet.since_created = str(int(delta.seconds/60/60)) + ' hours'
            elif int(delta.seconds/60/60)== 1:
                tweet.since_created = str(int(delta.seconds/60/60)) + ' hour'
            else:
                tweet.since_created = str(int(delta.seconds / 60 )) + ' minutes'
        else:
            if delta.days == 1:
                tweet.since_created = str(delta.days) + ' day'
            else:
                tweet.since_created = str(delta.days) + ' days'
    return render_template('dashboard.html', user=user, tweets=tweets)


@app.route('/profile')
def get_profile():
    user = User.query.get(int(session['userid']))
    return render_template('profile.html', user=user)


@app.route('/tweet/create', methods=['POST'])
def create_tweet():
    if 'userid' not in session:
        return redirect('/')
    if len(request.form['content']) > 255:
        flash('Tweet cannot be more than 255 characters', 'error')
    if len(request.form['content']) < 1:
        flash('Tweet cannot be empty', 'error')
    if not '_flashes' in session.keys():
        new_tweet = Tweet(content=request.form['content'], user_id=session['userid'])
        db.session.add(new_tweet)
        db.session.commit()
        return redirect('/dashboard')
    return redirect('/dashboard')


@app.route('/tweet/<id>/delete')
def delete_tweet(id):
    if 'userid' not in session:
        return redirect('/')
    tweet = Tweet.query.get(id)
    if tweet and tweet.user_id == session['userid']:
        db.session.delete(tweet)
        db.session.commit()
    return redirect('/dashboard')


@app.route('/tweet/<id>/like')
def like_tweet(id):
    if 'userid' not in session:
        return redirect('/')
    tweet = Tweet.query.get(id)
    user = User.query.get(session['userid'])
    user.tweets_this_user_likes.append(tweet)
    db.session.commit()
    return redirect('/dashboard')


@app.route('/tweet/<id>/unlike')
def unlike_tweet(id):
    if 'userid' not in session:
        return redirect('/')
    tweet = Tweet.query.get(id)
    user = User.query.get(session['userid'])
    user.tweets_this_user_likes.remove(tweet)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/tweet/<id>/edit')
def edit_tweet(id):
    if 'userid' not in session:
        return redirect('/')
    tweet = Tweet.query.get(id)
    if tweet and tweet.user_id == session['userid']:
        return render_template('edit.html', tweet=tweet)
    return render_template('edit.html', tweet=None)

@app.route('/tweet/<id>/update', methods=['POST'])
def update_tweet(id):
    if 'userid' not in session:
        flash('You are not logged in...', 'error')
        return redirect('/')
    if len(request.form['content']) < 1:
        flash('Tweet length cannot be 0', 'error')
    elif len(request.form['content']) > 255:
        flash('Tweet cannot be longer than 255 characters', 'error')
    if not '_flashes' in session.keys():
        if request.form['button'] == 'Update':
            tweet = Tweet.query.get(id)
            tweet.content = request.form['content']
            db.session.commit()
            return redirect('/dashboard')
        else:
            return redirect('/dashboard')
    return redirect('/tweet/{}/edit'.format(id))

@app.route('/users')
def choices():
    if 'userid' not in session:
        return redirect('/')
    users = User.query.all()
    for user in users:
        for follower in user.followers:
            if follower.id == session['userid']:
                user.followed_by_me = True
    return render_template('users.html', users=users)


@app.route('/users/<id>/unfollow')
def unfollow_user(id):
    if 'userid' not in session:
        return redirect('/')
    followed_user = User.query.get(id)
    follower = User.query.get(session['userid'])
    followed_user.followers.remove(follower)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<id>/follow')
def follow_user(id):
    if 'userid' not in session:
        return redirect('/')
    followed_user = User.query.get(id)
    follower = User.query.get(session['userid'])
    followed_user.followers.append(follower)
    db.session.commit()
    return redirect('/users')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            user = User.query.get(session['userid'])
            filename = '{}_'.format(user.id) + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if user.user_avatar:
                avatar = Avatar.query.get(user.user_avatar[0].id)
                delete_file = secure_filename(avatar.file_path)
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], delete_file))
                avatar.file_path = filename
                db.session.commit()
            else:
                new_file = Avatar(file_path='{}'.format(filename), user_id=user.id)
                db.session.add(new_file)
                db.session.commit()
            return redirect('/profile')
    return render_template('uploads.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)