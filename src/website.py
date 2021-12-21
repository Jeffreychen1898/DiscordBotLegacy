import flask
import waitress

@app.route("/")
def home():
    return "Bot should be running"

class Website:
    def __init__(self, name):
        global app
        app = flask.Flask(name)
    
    def run(self, serverPort):
        print("Website is online!")
        waitress.serve(app, port=serverPort)