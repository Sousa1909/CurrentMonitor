# Entry point for the WebApp
from app import app, socketio, cLog
from app.sockets import *

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)