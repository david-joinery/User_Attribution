import flask
import requests
from utils import count_words_at_url
import user_attribution_v2
from rq import Queue
from worker import conn
app = flask.Flask(__name__)
@app.route("/")

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())



def index():
	#return(user_attribution_v2)
	q = Queue(connection=conn)
	result = q.enqueue(count_words_at_url, 'http://heroku.com')

