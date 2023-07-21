# CurrentMonitor
MSc Project that consists in a Current Monitor using a Raspberry Pi Pico W.  
The objective of this project is to use concepts from MQTT (Publisher, Broker & Subscriber). The `Publisher`, our `Raspberry Pi Pico W`, publishes the values read by an AC Current Sensor to a `Broker` hosted in a VM. That very same VM will also host a webserver to which anyone can access to `Subscribe` to the content.

---
## What material do I need?
* To replicate this project you will need:  
  1. A Raspberry Pi Pico W -> [Information](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)
  2. An Analog Current Sensor -> [Like this one](https://www.dfrobot.com/product-1486.html)
  3. A Breadboard
  4. Some connector cables
  5. A source of AC current
   
---
## Is there anything I need to know?
* It is important to know some aspects about our `Raspberry Pi Pico W`:

![](Resources/pico_schematic.png)

* Relevant information for the context of the project:
  * Pins:
    * 39 - VSYS -> This is the input voltage, which can range from 2 to 5-volts, which is the Vcc pin we need/have to use since we need 5V to power the sensor.
    * 38 - GND -> A ground pin like any other, I just picked this one because it is close to the Vcc one (Yeah that's the reason 😎).
    * 31 - ADC0 -> We need a Analog pin for the data gathered by the sensor, which means we have 3 options (Pins: 31, 32 and 34).
  * Vagrant:
    * The VM we are going to be using is launched via [Vagrant](https://developer.hashicorp.com/vagrant).
      * This means:
          1. You need to [install VirtualBox](https://www.virtualbox.org/)
          2. You need to [install Vagrant](https://developer.hashicorp.com/vagrant/downloads), if you don't have it already.
          3. After installing all you have to do is:
             1. Run `vagrant up` in any terminal. This will create the VM according to the specifications in the `Vagrantfile` and the Shell scripts under `/scripts`.         
                > **Note**  
                > When running `vagrant up` make sure you are under the same directory as the `Vagrantfile` or else it won't work.  
                Additionally sometimes it is a good idea to run `vagrant provision` to force the execution of the shell scripts.
             2. When that is done if you want to access the VM's terminal all you have to do is run `vagrant ssh`.
                > **Note**  
                > If you want to exit the ssh all you have to do is run `exit` in the VM terminal. Additionally to turn off the VM simply run `vagrant halt` under the same directory as the `Vagrantfile`



---
## How do I put together all the physical components?
* Here is the connection diagram:  

![](Resources/schematic.png)

> **Warning**  
> You can only use the AC current sensor to clamp one of the terminals (positive or negative, it it the same) of your AC source, since they cancel each other out and if you were to clamp both you would be reading a null (as in 0) value.

---
## Project Structure

This project will have three major parts:
* Sensor + Raspberry Pi Pico W
  * This will act as a way to read the current value and publish it to the MQTT Broker
* The MQTT Broker
  * This will act as the intermediate between the Raspberry Pi Pico W and our Web Application.
* The Web Application
  * This is where all the collected data will be displayed.
  
### Sensor + Raspberry Pi Pico W

As stated before we will be collecting current values using an Analog Current Sensor and process that data using a Raspberry Pi Pico W. With this in mind lets break down the `currentSensor.py`. In this file there is all the code needed to run the process. You can find this file under the `/RaspPi` directory.  

The process flow described in this file:
1. The Raspberry Pi Pico W will need to connect to the local Wi-Fi. For that we created a method to do just that called `ConnectWifi`. This method has a particularity that we need to pass our current `location` as a parameter. The reasoning behind this is that since this project was done mainly in two locations (at home and at university) we didn't want to be changing the variables for the `ssid` and `password`, soo we added both credentials in the file and the correct credentials are used according to the parameter passed to the function.
   