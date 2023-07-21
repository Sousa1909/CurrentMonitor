import os
import sys
import logging as log
from flask import Flask
from flask_socketio import SocketIO
from pyngrok import ngrok
   
def logs():
    # Create a custom logger named 'app_logger'
    cLog = log.getLogger("app_logger")
    cLog.setLevel(log.DEBUG)

    # Create a file handler for the log file
    file_handler = log.FileHandler('./app.log')
    file_handler.setLevel(log.INFO)

    # Create a log formatter
    log_formatter = log.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_formatter)

    # Add the file handler to the custom logger
    cLog.addHandler(file_handler)

    return cLog

cLog = logs()   

##################### APP #####################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'key!'

# Initialize Flask-SocketIO
socketio = SocketIO(app)

# Initialize our ngrok settings into Flask
app.config.from_mapping(
    BASE_URL="http://localhost:5000",
    USE_NGROK=os.environ.get("USE_NGROK", "False") == "True" and os.environ.get("WERKZEUG_RUN_MAIN") != "true"
)

public_url = ngrok.connect(5000).public_url
cLog.info(" Generated NGROK Address: \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, 5000))
app.config["BASE_URL"] = public_url

# Import the routes.py and sockets.py files
from app import routes, sockets