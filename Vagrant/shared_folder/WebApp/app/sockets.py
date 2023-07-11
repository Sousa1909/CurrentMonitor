from app import socketio
import paho.mqtt.client as mqtt

mqtt_broker = 'localhost'
mqtt_topic = 'AMPS'

@socketio.on('connect')
def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')
    client.subscribe(mqtt_topic)

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')
    # Additional logic for handling client disconnection

def on_message_mqtt(client, userdata, msg):
    data = msg.payload.decode('utf-8')
    socketio.emit('mqtt_data', data)  # Emit data to WebSocket clients

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message_mqtt
client.connect(mqtt_broker, 1883, 60)
