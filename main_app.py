import flask
#import user_attribution_v2
app = flask.Flask(__name__)
@app.route("/")

def index():
	print('user-attribution-metrics')

