import flask
import user_attribution_v2
app = flask.Flask(__name__)
@app.route("/")

def index():
	return(user_attribution_v2)

