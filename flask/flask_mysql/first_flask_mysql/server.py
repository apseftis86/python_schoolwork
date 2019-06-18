from flask import Flask, render_template
from mysqlconnection import connectToMySQL  # import the function that will return an instance of a connection

app = Flask(__name__)


@app.route('/')
def index():
    mysql = connectToMySQL("first_flask")
    friends = mysql.query_db("SELECT * FROM friends;")
    print(friends)
    return render_template("index.html", all_friends = friends)

if __name__ == "__main__":
    app.run(debug=True)