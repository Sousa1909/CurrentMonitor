# Script that will be run by the Raspberry Pi Pico W

import time
import network
from machine import ADC, reset, Pin
from umqtt.simple import MQTTClient

#################################
#
#       WIFI CONNECTION
#
#################################

def connectWifi(location):
    """Connects to Wi-Fi

    Attempts to connect to local wifi, according to the value
    of the location (parameter) given. 
    If no connection is established raises an exception

    Args:
        location (str): Current location -> ("home" || "ipt") 

    Returns:
        bool: True or False if the connection was established
            successfully or not, respectively 
    """
    ssid_list = {
        'home_goncalo': 'Wi-Fi Sousa', 
        'home_joao': 'VITORPAULA',
        'ipt': 'TPSI'
    }    
    password_list = {
        'home_goncalo': 'Goncalo1909',
        'home_joao': '45159VITPA',
        'ipt': 'tpsi2022'
    }

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    try:
        if(location == "home_goncalo"):
            wlan.connect(
                ssid_list["home_goncalo"],
                password_list["home_goncalo"]
            )
        elif (location == "home_joao"):
            wlan.connect(
                ssid_list["home_joao"],
                password_list["home_joao"]
            )  
        elif (location == "ipt"):
            wlan.connect(
                ssid_list["ipt"],
                password_list["ipt"]
            )  
        else:
            raise ValueError("Unknown location given!")
        
        # Idles the RP while the wifi connection is not established
        while not wlan.isconnected():
            print("Waiting for connection...")
            time.sleep(2)
            machine.idle()

        # Connection Established
        print('''\
\nWLAN: connected!\n
      WiPy IP: {}
      NETMASK: {}
      GATEWAY: {}
      DNS:     {}\n'''.format(*wlan.ifconfig())
        )
        return True

    # Error
    except OSError:
        print("There was an error establishing connection")
        return False


#################################
#
#       DATA PROCESSING
#
#################################

# VREF stands for the reference Voltage (power to the sensor)
VREF = 5
# Maximum current range that the sensor can read 
AC_RANGE = 20 
# Amplification factor of the circuitry connected to the SCT013 sensor.
AMP_FACTOR = 2
# Used Analog Pin
ADC_PIN = machine.ADC(0)

def currentCalc():
    """Returns current sensor value

    Reads the Analog current value from the sensor and converts it into a digital Value

    Returns:
        float: Value of current in A (amps)
    """
    peak_voltage = 0

    for i in range(5):
        peak_voltage += ADC_PIN.read_u16()
        time.sleep_ms(1)

    peak_voltage /= 5

    voltage_virtual_value = (peak_voltage / 65535 * VREF) / AMP_FACTOR

    AC_current_value = voltage_virtual_value * AC_RANGE

    return AC_current_value

#################################
#
#             MQTT
#
#################################

# MQTT Broker IP Address
BRK_ADDR = '192.168.1.100'
# MQTT Client Id
CLIENT_ID = "Raspberry"
# MQTT Broker Username
BRK_USR = 'admin'
# MQTT Broker Password
BRK_PASSWD = 'admin'
# MQTT Publish Topic
PUB_TOPIC = 'AMPS'
# MQTT Subscribe Topic
SUB_TOPIC = 'STATUS'


def mqttConnect():
    """Establishes connection with the MQTT Broker

    Creates the instance of a MQTT client and attempts to establish
    a connection with the MQTT Broker

    Returns:
        MQTTClient: An instance of a MQTT Client
    """

    client = MQTTClient(
        CLIENT_ID,
        BRK_ADDR,
        user = BRK_USR,
        password = BRK_PASSWD,
        keepalive = 60
    )
    client.set_last_will(
        PUB_TOPIC,
        "Something went wrong! This is the Last Will message.",
        retain=False,
        qos=0
    )
    client.set_callback(mqttSubCallback)
    client.connect(clean_session=False)
    print('Connected to %s MQTT Broker\n'%(BRK_ADDR))

    return client

def mqttReconnect():
    """Reconnects with the MQTT Broker

    Attempts to reconnect to the MQTT Broker by resetting the RP

    Returns:
        void: --
    """
    time.sleep(5)
    machine.reset()

# Defines whether there is a publish of the sensor
# values or not
status = "True"

def mqttSubCallback(topic, msg):
    """Handles responses from MQTT Subscription

    Prints the content of the payload coming from the 
    MQTT subscription

    Returns:
        void: --
    """
    global status
    print("New message on topic: {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    # Change the state
    status = msg
    print("Publish status is now: ", msg, "\n")


#################################
#
#             MISC
#
#################################

#create LED object from pin13,Set Pin13 to output
LED = machine.Pin(
    "LED",
    machine.Pin.OUT
)  

def blink():
    """Blinks the LED

    Turns on the Raspberry Pi LED for a second and turns it
    off afterwards

    Returns:
        void: --
    """  
    LED.value(1) 
    time.sleep(1)
    LED.value(0)

#################################
#
#       RUN SYSTEM
#
#################################

def run():
    """Runs all functions

    Runs all functions in a sequential way so that the RP behaves
    as expected.

    Returns:
        void: --
    """
    connectedToWifi = False
    while connectedToWifi == False:
        connectedToWifi = connectWifi("home_goncalo")
    
    while True:
        try:
            client = mqttConnect()
            client.subscribe(SUB_TOPIC)
        except OSError:
            print("Failed to connect to the MQTT Broker. Attempting to reconnect...")
            mqttReconnect()

        while True:
            try:
                client.check_msg()
                if (status == "True"):
                    toPublish =  currentCalc()
                    print("Value: ", toPublish, "A")
                    client.publish(
                        PUB_TOPIC,
                        msg=str(toPublish)
                        )
                    blink()
                    print('Published to MQTT Broker successfully!\n')
                else:
                    print("The Web Client turned off sensor data gathering!\n")
                time.sleep(10)
            except:
                print("Something went wrong with the connection! Attempting to reconnect...")
                mqttReconnect()
                pass
# :)
run()