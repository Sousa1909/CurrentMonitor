import random
import json
import os
from datetime import datetime
from app import app, socketio, cLog
from flask_mqtt import Mqtt

#TODO: change the names of these variables
broker_topic = "AMPS"

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'admin'
app.config['MQTT_PASSWORD'] = 'admin'
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    cLog.info("Connected to the MQTT")
    mqtt.subscribe(broker_topic)

@mqtt.on_disconnect()
def handle_disconnect():
    cLog.info("CLIENT DISCONNECTED")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    cLog.info(f"Raspberry Pi Message Payload: {data}")
    socketio.emit(
        'mqtt_data',
        data=data
    )
    # Save data to JSON file with timestamp
    saveToJson(data)

@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    cLog.info(f"WebApp Message Payload: {data}")
    mqtt.publish(
        data['topic'],
        data['message']
    )

@socketio.on('disconnect')
def on_disconnect():
    cLog.info('Client disconnected from SocketIO')

def saveToJson(data):
    # Add timestamp to the data dictionary
    data_with_timestamp = {
        'timestamp': datetime.now().isoformat(),
        'topic': data['topic'],
        'payload': data['payload']
    }
    
    # Get the current working directory
    current_directory = os.getcwd()

    # Create the relative path to the data.json file
    relative_path = os.path.join(current_directory, 'app/data', 'data.json')

    # Save data to JSON file
    try:
        # Check if the file exists and is not empty
        if os.path.exists(relative_path) and os.path.getsize(relative_path) > 0:
            # Read existing data from the file
            with open(relative_path, 'r') as file:
                existing_data = json.load(file)
        else:
            # Initialize as an empty list if the file is empty or doesn't exist
            existing_data = []
        
        # Append the new data to the existing data
        existing_data.append(data_with_timestamp)

        with open(relative_path, 'w') as file:
            json.dump(
                existing_data,
                file,
                indent=2
            )
            file.write('\n')
    except IOError as e:
        cLog.error(f"Error writing to JSON file: {e}")
