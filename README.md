# Artemis-cc
This repository contains software that was created when developing a hardware platform for the [ArtEmis project](https://www.artemisproject.eu/). The repository has code for two platforms, one based on a Raspberry PI 4 and one based on the radio-sensors S2 controller. It was created by [Axel Karlsson](https://www.github.com/acke-k) and [Frej Larssen](https://www.github.com/frejlarssen) for their bachelor thesis.
## Raspberry pi
This platform is based on a Raspberry PI 4 and a [simcom 7080 hat by WaveShare.](https://www.waveshare.com/sim7080g-cat-m-nb-iot-hat.htm).
The hat is mounted on and connected via a micro USB cable. The software can be found in the directory artemis-rpi.
### Building
*These instructions are taken from the [WaveShare wiki](https://www.waveshare.com/wiki/SIM7080G_Cat-M/NB-IoT_HAT). Visit that page for detailed instructions.*
To run the program, you must first install the packages RPi.GPIO and python-serial. This can be done by the commands below:
```
sudo pip install RPi.GPIO
sudo apt-get install python-serial
```
Then, the pi_gpio_init.sh must be run:
```
sh ./artemis-rpi/pi_gpio_init.sh 
```
Lastly, enable the UART port by typing the following command
```
rapsi-config
```
and selecting *options->serial->open hardware serial port*.

Now, send a MQTT message using
```
python3 rpi-mqtt.py -h <URL of broker> -p <port> -t <topic of the message> -m <the message>
```
## radio-sensors s2
This platform is based on the [radio-sensors s2](http://radio-sensors.com/) controller and a sim7000G. The platform was originally developed by Robert Olsson and Peter Sjödin at KTH.
The software is based on a fork of Riot OS by Peter Sjödin, which implements MQTTSN on the platform. A simple application has been built using the API provided in the fork. The code can be found in the directory artemis-rs.
### Building
The repository contains the correct version of Riot OS. To download it, go into the repo and run the commands
```
git submodule init
git submodule update
```
To build the application go into the application directory and flash the program using the makefile:
```
cd artemis-rs/app
make BOARD=avr-rss2 PORT=<port where the board is connected> flash
```
The application can communicate with the computer via a shell running over the serial port. There are many programs that can do this, we used minicom when developing this application. After configuring the communication MQTT messages can be sent with the following command:
```
<url of broker> <port> <topic of message> <message>
```
