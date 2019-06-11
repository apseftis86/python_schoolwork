from flask import Flask  # Import Flask to allow us to create our app
app = Flask(__name__)    # Create a new instance of the Flask class called "app"
@app.route('/')          # The "@" decorator associates this route with the function immediately following
def hello_world():
    return 'Hello World!'  # Return the string 'Hello World!' as a response
@app.route('/dojo')
def dojo():
    return 'Dojo!'
@app.route('/say/<name>')
def say_name(name):
    return "Hi " + str(name) + "!"
@app.route('/repeat/<number>/<word>')
def return_string(number, word):
    my_num = int(number)
    my_str = ''
    for x in range(my_num):
        my_str += word
    return my_str
@app.errorhandler(404)
def page_not_found(error):
    return "Sorry! No reponse. Try again."

if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)    # Run the app in debug mode.
