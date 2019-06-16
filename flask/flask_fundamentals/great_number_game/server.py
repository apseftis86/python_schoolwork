from flask import Flask, render_template, request, redirect, session
import random
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'  # set a secret key for security purposes

@app.route('/')
def number_game():
    if 'random_number' in session:
        pass
    else:
        session['random_number'] = random.randint(1,100)
        session['attempts'] = 0
    if 'leaders' not in session:
        session['leaders'] = []
    return render_template('index.html', attempts=session['attempts'], )


@app.route('/difficulty', methods=['POST'])
def set_difficulty():
    session['difficulty'] = request.form['difficulty']
    session['started'] = True
    if session['difficulty'] == 'five':
        session['attempts_remaining'] = 5
    else:
        session['attempts_remaining'] = 'infinite'
    return redirect('/')


@app.route('/guess', methods=['POST'])
def guessing():
    session['attempts'] += 1
    if session['attempts_remaining'] != 'infinite':
        session['attempts_remaining'] -= 1
        if session['attempts_remaining'] == 0:
            return redirect('/game-over')
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


@app.route('/game-over')
def game_over():
    return render_template('game_over.html')

@app.route('/leaderboard')
def leaderboard():
    if 'leaders' not in session:
        leaders = ''
    else:
        leaders = session['leaders']
    return render_template('leaderboard.html', leaders=leaders)


@app.route('/add-leader', methods=['POST'])
def add_winner():
    session['leader_added'] = True
    new_leader = {
        "name": request.form['leader_name'],
        "attempts": session['attempts']
    }
    leader_list = session['leaders']
    leader_list.append(new_leader)
    session['leaders'] = leader_list
    return redirect('/leaderboard')


@app.route('/reset', methods=['POST'])
def reset():
    leaders = session['leaders']
    session.clear()
    session['leaders'] = leaders
    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)