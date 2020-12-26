from flask import Flask

app = Flask(__name__)

@app.route('/getData')
def getData():
    pass