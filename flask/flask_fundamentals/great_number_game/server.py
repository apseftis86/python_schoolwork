from flask import Flask, render_template, request, redirect, session
import random
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'  # set a secret key for security purposes

@app.route('/')
def number_game():
    if 'random_number' not in session:
        session['random_number'] = random.randint(1,100)
        session['attempts'] = 0
        session['started'] = True
        session['guessed'] = False
    if 'leaders' not in session:
        # setting to array at the beginning allows for append
        # method when adding to the leader board
        session['leaders'] = []
    return render_template('index.html', attempts=session['attempts'])

""" sensei bonus I believe
@app.route('/difficulty', methods=['POST'])
def set_difficulty():
    session['difficulty'] = request.form['difficulty']
    session['started'] = True
    if session['difficulty'] == 'five':
        session['attempts_remaining'] = 5
    else:
        session['attempts_remaining'] = 'infinite'
    return redirect('/')
"""


@app.route('/guess', methods=['POST'])
def guessing():
    session['attempts'] += 1
    """ bonus stuff 
    if session['attempts_remaining'] != 'infinite':
        session['attempts_remaining'] -= 1
        if session['attempts_remaining'] == 0:
            return redirect('/game-over')
    """
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
        session['leaders'] = []
    return render_template('leaderboard.html', leaders=session['leaders'])


@app.route('/add-leader', methods=['POST'])
def add_winner():
    # The true session key was so once they added their name
    # once they could not add it again
    if session['guessed']:
        session['leader_added'] = True
        new_leader = {
            "name": request.form['leader_name'],
            "attempts": session['attempts']
        }
        session['leaders'].append(new_leader)
        return redirect('/leaderboard')
    # also redirect just so they cant do a POST with their
    # information and cheat
    else:
        return redirect('/leaderboard')


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    # Tim did look over my code and tell me you can clear specific keys not to clear leaders
    # but code wise I think its easier to set leaders to a variable clear everything else
    # and just set leaders back again since my keys are
    # started, attempts, guessed, leader_added... not sure you can pop those all on the
    # same session.pop() so I think this is an okay way...

    leaders = session['leaders']
    session.clear()
    session['leaders'] = leaders
    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)