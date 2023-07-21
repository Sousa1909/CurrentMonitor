import random
import json
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
    cLog.info(f"Message Payload: {data}")
    socketio.emit('mqtt_data', data=data)

@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message'])

@socketio.on('disconnect')
def on_disconnect():
    cLog.info('Client disconnected from SocketIO')
