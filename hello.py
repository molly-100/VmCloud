from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/")
def hello2():
    return "Say Hello from Dockerised Flask"

@app.route("/route32a")
def route32a():
    return "Hello from the 32A"

@app.route("/route")
def route():
    number=request.args.get('number')
    return "Hello from the {}".format(number)

@app.route("/cc")
def cc():
    return "Hello Cloud Computing, this is a Dockerised Flask"


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')
