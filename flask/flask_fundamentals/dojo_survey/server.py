from flask import Flask, render_template, request, redirect
app = Flask(__name__)
# our index route will handle rendering our form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def create_user():
    lang_list = []
    print('Got Post Info')
    print('request.form')
    name_from_form = request.form['name']
    location_from_form = request.form['location']
    fave_lang = request.form['fave_language']
    level_from_form = request.form['level']
    comment_from_form = request.form['comment']
    known_languages = request.form.getlist('known_languages[]')
    return render_template('result.html', name=name_from_form, location=location_from_form,
                           languages=known_languages, fave_language=fave_lang, level=level_from_form,
                           comment=comment_from_form)

if __name__ == "__main__":
    app.run(debug=True)