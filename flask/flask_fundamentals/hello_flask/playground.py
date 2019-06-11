from flask import Flask, render_template
app = Flask(__name__)

@app.route('/play')
def play():
    return render_template('play.html', boxes=3)


@app.route('/play/<number>')
def play_number(number):
    return render_template('play.html', boxes=int(number))


@app.route('/play/<number>/<color>')
def play_number_color(number, color):
    return render_template('play.html', boxes=int(number), box_color=str(color))

if __name__=="__main__":
    app.run(debug=True)
