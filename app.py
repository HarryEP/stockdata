from flask import Flask, render_template

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route("/")
def index():
    return render_template('index.html'), 200


@app.route("/analysis")
def show_analysis():
    return "Analysis shown here", 200


if __name__ == "__main__":
    app.run(debug=True)
