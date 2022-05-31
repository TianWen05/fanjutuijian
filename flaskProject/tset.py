from flask import render_template, Flask, request, url_for, session, flash, g
import recommend
app = Flask(__name__)


@app.route("/")
def home():
    n = recommend.recommendRandom(1)


