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


def run_server():
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(('8.8.8.8', 80))
    app.run(host=socket.gethostname(), port=80, debug=True)
