import os
import sys
from flask import Flask                             # 15:52
from flask_socketio import SocketIO
#from flask_ngrok import run_with_ngrok
from pyngrok import ngrok

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize Flask-SocketIO
socketio = SocketIO(app)

# Initialize our ngrok settings into Flask
app.config.from_mapping(
    BASE_URL="http://localhost:5000",
    USE_NGROK=os.environ.get("USE_NGROK", "False") == "True" and os.environ.get("WERKZEUG_RUN_MAIN") != "true"
)

public_url = ngrok.connect(5000).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, 5000))
app.config["BASE_URL"] = public_url


# Import the routes.py and sockets.py files
from app import routes, sockets