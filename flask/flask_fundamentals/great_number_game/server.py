from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import random
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes

@app.route('/')
def number_game():
    if 'random_number' in session:
        pass
    else:
        session['random_number'] = random.randint(1,100)
    return render_template('index.html')
@app.route('/guess', methods=['POST'])
def guessing():
    user_guess = int(request.form['guess'])
    if user_guess > session['random_number']:
        session['response'] = 'Too High'
        session['response_box_color'] = 'response_box_red'
    elif user_guess < session['random_number']:
        session['response'] = 'Too Low'
        session['response_box_color'] = 'response_box_orange'
    elif user_guess == session['random_number']:
        session['guessed'] = True
        session['response_box_color'] = 'response_box_green'
    return redirect('/')
@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')
if __name__=="__main__":
    app.run(debug=True)