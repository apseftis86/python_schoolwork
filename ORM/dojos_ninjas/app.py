from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
app = Flask(__name__)
# configurations to tell our app about the database we'll be connecting to
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dojos_ninjas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# a tool for allowing migrations/creation of tables
migrate = Migrate(app, db)
#### ADDING THIS CLASS ####
# the db.Model in parentheses tells SQLAlchemy that this class represents a table in our database
class Ninja(db.Model):
    __tablename__ = "ninjas"    # optional
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    dojo_id = db.Column(db.Integer, db.ForeignKey("dojos.id"), nullable=True)
    dojo = db.relationship('Dojo', foreign_keys=[dojo_id], backref="ninja_dojo", cascade="all")
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Dojo(db.Model):
    __tablename__ = "dojos"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    city = db.Column(db.String(45))
    state = db.Column(db.String(45))

@app.route('/')
def index():
    all_dojos = Dojo.query.all()
    all_ninjas = Ninja.query.all()
    return render_template('index.html', dojos=all_dojos, ninjas=all_ninjas)

@app.route('/dojos')
def dojos():
    all_dojos = Dojo.query.all()
    return render_template('dojos.html', dojos=all_dojos)

@app.route('/dojos/<id>/destroy')
def destroy_dojo(id):
    dojo = Dojo.query.get(int(id))
    db.session.delete(dojo)
    db.session.commit()
    return redirect('/dojos')

@app.route('/ninjas/<id>/destroy')
def destroy_ninja(id):
    ninja = Ninja.query.get(int(id))
    db.session.delete(ninja)
    db.session.commit()
    return redirect('/ninjas')

@app.route('/ninjas')
def ninjas():
    all_dojos = Dojo.query.all()
    all_ninjas = Ninja.query.all()
    return render_template('ninjas.html', ninjas=all_ninjas, dojos=all_dojos)

@app.route('/create-ninja', methods=['POST'])
def create_ninja():
    new_ninja = Ninja(first_name=request.form['first_name'],
                    last_name=request.form['last_name'], dojo_id=request.form['dojo_id'])
    db.session.add(new_ninja)
    db.session.commit()
    if request.form['page'] == 'ninjas':
        return redirect('/ninjas')
    return redirect('/')

@app.route('/create-dojo', methods=['POST'])
def create_dojo():
    new_dojo = Dojo(name=request.form['name'],
                    city=request.form['city'], state=request.form['state'])
    db.session.add(new_dojo)
    db.session.commit()
    if request.form['page'] == 'dojos':
        return redirect('/dojos')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)