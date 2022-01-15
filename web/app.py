import socket

from flask import Flask, render_template
from flask_talisman import Talisman

app = Flask(__name__)

Talisman(app)


@app.route('/')
def home():
    return render_template('errors/404.html')


@app.route('/predict', methods=['POST'])
def predict():
    pass


"""ssl_context="adhoc"""
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    app.run(host=s.getsockname()[0], port=80, debug=True)
