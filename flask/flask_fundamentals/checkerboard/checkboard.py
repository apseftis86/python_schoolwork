from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def checker_default():
    return render_template("index.html", x_rows=int(8), y_rows=int(8))


@app.route('/<x>')
def checker_x(x):
    return render_template("index.html", x_rows=int(x), y_rows=int(1))

@app.route('/<x>/<y>')
def checker_x_y(x, y):
    return render_template("index.html", x_rows=int(x), y_rows=int(y))

@app.route('/<x>/<y>/<color1>/<color2>')
def checker_x_y_colors(x, y, color1, color2):
    return render_template("index.html", x_rows=int(x), y_rows=int(y), color1=color1, color2=color2)

if __name__=="__main__":
    app.run(debug=True)
