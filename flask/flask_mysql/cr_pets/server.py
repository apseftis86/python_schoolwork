from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL  # import the function that will return an instance of a connection

app = Flask(__name__)


@app.route('/')
def index():
    mysql = connectToMySQL("pet_database") # this holds the name to my database
    pets = mysql.query_db("SELECT * FROM pets;")
    print(pets)
    return render_template("index.html", all_pets = pets)


@app.route('/add-pet', methods=['POST'])
def add_new_pet():
    db = connectToMySQL("pet_database") # this holds the name to my database
    query = "INSERT INTO pets (name, type, created_at) VALUES (%(n)s, %(t)s, now());"
    data = {
        "n": request.form['name'],
        "t": request.form['type'],
    }
    new_pet_id = db.query_db(query, data)
    print(new_pet_id)
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)