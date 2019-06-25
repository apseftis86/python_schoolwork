from config import app
from controller_functions import index, dojos, destroy_dojo, create_dojo, ninjas, destroy_ninja, create_ninja

app.add_url_rule('/', view_func=index)
app.add_url_rule('/dojos', view_func=dojos)
app.add_url_rule('/dojos/<id>/destroy', view_func=destroy_dojo)
app.add_url_rule('/create-dojo', view_func=create_dojo, methods=['POST'])
app.add_url_rule('/ninjas', view_func=ninjas)
app.add_url_rule('/ninjas/<id>/destroy', view_func=destroy_ninja)
app.add_url_rule('/create-ninja', view_func=create_ninja,  methods=['POST'])
