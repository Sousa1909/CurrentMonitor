# Script that will be run by the Raspberry Pi Pico W

import time
import network
from machine import ADC
from umqttsimple import MQTTClient, reset

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
        'home': 'Wi-Fi Sousa',
        'ipt': 'TPSI'
    }    
    password_list = {
        'home': 'Goncalo1909',
        'ipt': 'tpsi2022'
    }

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    try:
        if(location == "home"):
            wlan.connect(
                ssid_list["home"],
                password_list["home"]
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
            machine.idle()

        # Connection Established
        print('''\
WLAN: connected!
      WiPy IP: {}
      NETMASK: {}
      GATEWAY: {}
      DNS:     {}'''.format(*wlan.ifconfig())
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

# VREF stand for the reference Voltage (power to the sensor)
VREF = 5
# Maximum current range that the sensor can read 
ACTDetectionRange = 20 
# Amplification factor of the circuitry connected to the SCT013 sensor.
amplification_factor = 2
# Used Analog Pin
adc_pin = machine.ADC(0)

def currentCalc():
    """Returns current sensor value

    Reads the Analog current value from the sensor and converts it into a digital Value

    Returns:
        float: Value of current in A (amps)
    """
    peak_voltage = 0

    for i in range(5):
        peak_voltage += adc_pin.read_u16()
        time.sleep_ms(1)

    peak_voltage /= 5

    voltage_virtual_value = (peak_voltage / 65535 * VREF) / amplification_factor

    AC_current_value = voltage_virtual_value * ACTDetectionRange

    return AC_current_value

#################################
#
#       MQTT PUBLISH
#
#################################

# MQTT Broker IP Address
broker_addr = '192.168.1.100'
# MQTT Client Id
broker_cid = "Raspberry"
# MQTT Broker Username
broker_usr = 'admin'
# MQTT Broker Password
broker_pswrd = 'admin'
# MQTT Topic
broker_topic = 'AMPS'

def mqttConnect():
    """Establishes connection with the MQTT Broker

    Creates the instance of a MQTT client and attempts to establish
    a connection with the MQTT Broker

    Returns:
        MQTTClient: An instance of a MQTT Client
    """
    client = MQTTClient(
        broker_cid,
        broker_addr,
        user = broker_usr,
        password = broker_pswrd,
        keepalive = 60
    ).connect()
    print('Connected to %s MQTT Broker'%(broker_addr))
    return client

def mqttReconnect():
    """Reconnects with the MQTT Broker

    Attempts to reconnect to the MQTT Broker by resetting the RP

    Returns:
        void: --
    """
    print('Failed to connected to the MQTT Broker. Attempting to reconnect...')
    time.sleep(5)
    machine.reset()

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
        connectedToWifi = connectWifi("home")
    
    while True:
        try:
            client = mqttConnect()
        except OSError:
            print("Failed to connect to the MQTT Broker. Attempting to reconnect...")
            mqttReconnect()

        while True:
            try:
                toPublish = str("Value: ", currentCalc(), "A\n")
                print(toPublish)
                client.publish(
                    broker_topic,
                    msg= toPublish
                    )
                print('Published to MQTT Broker Successfully!')
                time.sleep(3)
            except:
                print("Something went wrong with the connection! Attempting to reconnect...")
                mqttReconnect()
# :)
run()