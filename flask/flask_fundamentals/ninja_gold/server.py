from flask import Flask, render_template, request, redirect, session
import random
import datetime
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'  # set a secret key for security purposes


@app.route('/')
def index():
    if 'gold' not in session:
        session['gold'] = 0
    if 'activities' not in session:
        session['activities'] = []
    history = session['activities']
    return render_template('index.html', gold=session['gold'], history=history)


@app.route('/process-money', methods=['POST'])
def process_money():
    location = request.form['location']
    if location == 'casino':
        processing = random.randint(-50, 50)
    elif location == 'farm':
        processing = random.randint(10, 20)
    elif location == 'cave':
        processing = random.randint(5, 10)
    else:
        processing = random.randint(2, 5)
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