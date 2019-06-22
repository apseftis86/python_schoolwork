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

    """ this was for sensei bonus losing after a certain amount of time.
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
    """
    return render_template('index.html', gold=session['gold'], history=session['activities'])


@app.route('/process-money', methods=['POST'])
def process_money():
    """ this was for sensei bonus not to use the conditionals
    money_values = {
        'farm': [10, 20],
        'casino': [-50, 50],
        'house': [2, 5],
        'cave': [5, 10]
    }
    processing = random.randint(money_values[request.form['location']][0], money_values[request.form['location']][1])
    """

    """  the block below is going to be to get the location from the html form and 
    determine how much money you will lose or gain from it... if you see above to not 
    do the conditionals I used a dictionary instead """

    location = request.form['location']
    if location == 'farm':
        processing = random.randint(10, 20)
    if location == 'cave':
        processing = random.randint(5, 10)
    if location == 'house':
        processing = random.randint(2, 5)
    if location == 'casino':
        processing = random.randint(-50, 50)

    session['gold'] = int(session['gold']) + processing

    """ I used this code below to determine the type of activity so I could 
    make the class in my css reflect the right color """

    if processing < 0:
        action = 'loss'
    elif processing > 0:
        action = 'gain'
    else:
        action = 'null'
    new_activity = {
        "location": location,
        "type": action,
        "amount": processing,
        "timestamp": datetime.datetime.now()
    }
    session['activities'].append(new_activity)
    return redirect('/')


@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)