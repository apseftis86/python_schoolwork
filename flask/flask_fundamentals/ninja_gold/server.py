from flask import Flask, render_template, request, redirect, session
import random
import datetime
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'  # set a secret key for security purposes


@app.route('/')
def index():
    if 'activities' not in session:
        session['activities'] = []
        session['choices'] = 0
        session['over'] = False
    if 'gold' not in session:
        session['gold'] = 0
    else:
        if session['choices'] < 15:
            if session['gold'] >= 200:
                session['over'] = True
                session['response'] = 'You win!'
            elif session['gold'] <= -100:
                session['over'] = True
                session['response'] = 'You lose...'
        else:
            session['over'] = True
            session['response'] = 'You lose...'
    history = session['activities']
    return render_template('index.html', gold=session['gold'], history=history)


@app.route('/process-money', methods=['POST'])
def process_money():
    money_values = {
        'farm': [10, 20],
        'casino': [-50, 50],
        'house': [2, 5],
        'cave': [5, 10]
    }
    if session['over']:
        return redirect('/')
    session['choices'] += 1
    location = request.form['location']
    processing = random.randint(money_values[request.form['location']][0], money_values[request.form['location']][1])
    session['gold'] = int(session['gold']) + processing
    if processing < 0:
        action = 'loss'
    elif processing > 0:
        action = 'gain'
    else:
        action = 'null'
    activities = session['activities']
    new_activity = {
        "location": location,
        "type": action,
        "amount": processing,
        "timestamp": datetime.datetime.now()
    }
    activities.append(new_activity)
    session['activities'] = activities
    return redirect('/')


@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)