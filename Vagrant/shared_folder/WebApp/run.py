from app import app, socketio
from app.sockets import *

if __name__ == '__main__':
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    socketio.run(app, debug=True)
    #try:
        # Run the Flask-SocketIO app
        #socketio.run(app, debug=True)
    
    #finally:
        #client.loop_stop()