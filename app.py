from flask import Flask, render_template

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route("/")
def index():
    return "Use this program to find out about stock data", 200
