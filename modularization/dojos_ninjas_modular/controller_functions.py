# flask imports
from flask import render_template, request, redirect
# database imports
from config import db
from models import Ninja, Dojo

def index():
    all_dojos = Dojo.query.all()
    all_ninjas = Ninja.query.all()
    return render_template('index.html', dojos=all_dojos, ninjas=all_ninjas)

# dojo functions
def dojos():
    all_dojos = Dojo.query.all()
    return render_template('dojos.html', dojos=all_dojos)

def create_dojo():
    new_dojo = Dojo(name=request.form['name'],
                    city=request.form['city'], state=request.form['state'])
    db.session.add(new_dojo)
    db.session.commit()
    if request.form['page'] == 'dojos':
        return redirect('/dojos')
    return redirect('/')

def destroy_dojo(id):
    dojo = Dojo.query.get(int(id))
    db.session.delete(dojo)
    db.session.commit()
    return redirect('/dojos')

# ninja functions
def ninjas():
    all_dojos = Dojo.query.all()
    all_ninjas = Ninja.query.all()
    return render_template('ninjas.html', ninjas=all_ninjas, dojos=all_dojos)

def create_ninja():
    new_ninja = Ninja(first_name=request.form['first_name'],
                    last_name=request.form['last_name'], dojo_id=request.form['dojo_id'])
    db.session.add(new_ninja)
    db.session.commit()
    if request.form['page'] == 'ninjas':
        return redirect('/ninjas')
    return redirect('/')


def destroy_ninja(id):
    ninja = Ninja.query.get(int(id))
    db.session.delete(ninja)
    db.session.commit()
    return redirect('/ninjas')