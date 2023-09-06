# Artemis-cc
This repository contains software that was created when developing a hardware platform for the [ArtEmis project](https://www.artemisproject.eu/). The repository has code for two platforms, one based on a Raspberry Pi 4 and one based on the radio-sensors S2 controller. It was created by [Axel Karlsson](https://www.github.com/acke-k) and [Frej Larssen](https://www.github.com/frejlarssen) for their bachelor thesis.
## Raspberry Pi
This platform is based on a Raspberry PI 4 model B and a [simcom 7080 hat by WaveShare](https://www.waveshare.com/sim7080g-cat-m-nb-iot-hat.htm).
The hat is mounted on and connected via a micro USB cable. The software can be found in [artemis-rpi](/artemis-rpi/).
### Building
*These instructions are taken from the [WaveShare wiki](https://www.waveshare.com/wiki/SIM7080G_Cat-M/NB-IoT_HAT). Visit that page for detailed instructions.*
To run the program, you must first install the packages RPi.GPIO and python-serial. This can be done by the commands below:
```
sudo pip install RPi.GPIO
sudo apt-get install python-serial
```
Then, the `pi_gpio_init.sh` must be run:
```
sh ./artemis-rpi/pi_gpio_init.sh 
```
Lastly, enable the UART port by typing the following command
```
rapsi-config
```
and selecting *options->serial->open hardware serial port*.

Connect the UART pins on the Raspberry Pi to another device that can simulate a sensor. We used another Raspberry Pi. Go through the same process as above for the sensor RPi and connect the RX pin to the TX pin and vice versa.

Run the script [sensor-rpi.py](/artemis-rpi/sensor-rpi.py) on the Raspberry Pi that simulates the sensor. Change the port in the line `port = '/dev/ttyS0'` if needed. There are three commands that you can run with the script:

```
sensor-rpi.py send <topic> <message>
```
Sends a topic and a message to the RPi with the radio. The message are published to the topic immediately.
```
sensor-rpi.py many <topic> <number of messages> <sleep between messages>
```
Same as above but does so a number of times with a delay in between. (One UART-message for each message to publish.)
```
sensor-rpi.py loop <topic> <number of messages> <sleep between messages>
```
Instructs the RPi with the radio to start an internal loop that publishes a number of messages with a delay between each. (Only one UART-message.)
## radio-sensors s2
This platform is based on the [radio-sensors s2](http://radio-sensors.com/) controller (henceforth called rs2) and a sim7000G. The platform was originally developed by [Robert Olsson](https://github.com/herjulf) and [Peter Sjödin](https://github.com/posjodin) at KTH.
The software is based on a fork of Riot OS by Peter Sjödin, which implements MQTT-SN on the platform. A simple application has been built using the API provided in the fork. The code that runs on the radio sensor node can be found in the `MQTTSN-Publisher` directory.
### Building
The repository contains the correct version of Riot OS. To download it, go into the repo and run the commands
```
git submodule init
git submodule update
```
To build the application go into the application directory and flash the program using the makefile:
```
cd MQTTSN-Publisher/app
make BOARD=avr-rss2 PORT=<port where the board is connected> flash
```
### Provide input for the node
The application can communicate with the computer via a shell running over the serial port. The Python script [sensor-rs2.py](/sensor-rs2.py) sends data to the rs2 node.
Run the script as follows:
```
python3 sensor-rs2.py <port where the board is connected> <baudrate>
```
The rs2 communicates with the baudrate 115200.

Uncomment function calls in [sensor-rs2.py](/sensor-rs2.py) to send messages in different ways (see code documentation).
