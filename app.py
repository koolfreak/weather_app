
import json
import urllib.request
from flask import Flask, render_template, abort, request

app = Flask(__name__)

@app.route('/')
def weather():  # put application's code here

    return render_template("index.html", data={})

@app.route("/forecast/current", methods=['POST'])
def forecast():

    pass

if __name__ == '__main__':
    app.run(debug=True)
