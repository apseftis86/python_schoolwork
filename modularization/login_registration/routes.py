from config import app
from controller_functions import index, login, register, dashboard, logout

app.add_url_rule('/', view_func=index)
app.add_url_rule('/login', view_func=login, methods=['POST'])
app.add_url_rule('/register', view_func=register, methods=['POST'])
app.add_url_rule('/dashboard', view_func=dashboard)
app.add_url_rule('/logout', view_func=logout)
