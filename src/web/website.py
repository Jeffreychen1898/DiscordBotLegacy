import flask
import waitress

app = flask.Flask(__name__)

@app.route("/")
def home():
    return "Bot should be running"

def run_website(port_number):
    print("Website is online!")
    waitress.serve(app, port=port_number)
