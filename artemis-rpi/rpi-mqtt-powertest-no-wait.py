#!/usr/bin/python

#
#   This program tests MQTT commands
#
import sys
import RPi.GPIO as GPIO
import serial
import time
import getopt

power_key = 7

# power on simcom module
def power_on(power_key):
    print('simcom starting')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(power_key,GPIO.OUT)
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(power_key,GPIO.LOW)
    print('startup done')

# power down simcom module
def power_down(power_key):
    print('SIM7080X is loging off:')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(power_key,GPIO.OUT)
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(power_key,GPIO.LOW)
    print('Good bye')

# run to make sure that module has started
# timeout: number of seconds to wait for start, if 0 wait infinite amount of time
def checkStart(timeout):
    print('Checking if simcom started')
    # loop until response
    ser.write( 'AT\r\n'.encode() )
    while True:
        timeout -= 1
        time.sleep(1)
        if ser.in_waiting != 0:
            recBuff = ser.read(ser.in_waiting)
            print('SOM7080G responded: ' + recBuff.decode())
            if 'OK' in recBuff.decode():
                recBuff = ''
                break 
        if timeout == 0:
            print('timed out at start')
            break

# send AT command to simcom
# command: AT command   timeout: timeout for answer, if 0 wait infinite amount of time
def send_command(command, timeout):
    ser.write((command + '\r\n' ).encode())
    while True:
        timeout -= 1
        time.sleep(0.1)
        rec_buff = ''
        if ser.in_waiting:
            time.sleep(0.01)
            rec_buff = ser.read(ser.in_waiting)
            break
        if rec_buff != '':
            print(rec_buff.decode())
        if timeout == 0:
            break
    if rec_buff != '':
        print('Response: ' + rec_buff.decode())
    else:
        print('No response')

def send_mqtt(host, port, topic, message):
    # Establish connection and send message
    print('Select LTE mode')
    send_command('AT+CNMP=38', 5)
    print('Activate network bearing')
    send_command('AT+CNACT=0,1', 3)
    print('Set TCP index')
    send_command('AT+CACID=0', 3)
    
    print('Set broker')
    send_command('AT+SMCONF=\"URL\",\"' + host + '\",\"' + port + '\"', 3)
    print('Set keeptime')
    send_command('AT+SMCONF=\"KEEPTIME\",60', 3)
    print('Set cleanss')
    send_command('AT+SMCONF=\"CLEANSS\",1', 3)
    print('Set topic')
    send_command('AT+SMCONF=\"TOPIC\",\"' + topic + '\"',3)
    print('Set message')
    send_command('AT+SMCONF=\"MESSAGE\",\"' + message + '\"',3)
    
    print('Connect to server')
    send_command('AT+SMCONN', 25)
    print('Disconnect')
    send_command('AT+SMDISC', 3)
    print('Deactivate network bearing')
    send_command('AT+CNACT=0,0', 3)
    
    print('All done!')

def main(argv):
    host = ''
    port = ''
    topic = ''
    msg = ''

    opts, args = getopt.getopt(argv, "h:p:t:m:", [])
    for opt,arg in opts:
        if opt in ("-h"):
            host = arg
        elif opt in ("-p"):
            port = arg
        elif opt in ("-t"):
            topic = arg
        elif opt in ("-m"):
            msg = arg
        else:
            print('Usage: cc-rpi.py -h <host> -p <port> -t <topic> -m <message>')
    print("host: ", host)
    print("port: ", port)
    print("topic: ", topic)
    print("message: ", msg)
        
    send_mqtt(host, port, topic, msg)
if __name__ == "__main__":
    try:
        if (len(sys.argv) != 9):
            print('Usage: cc-rpi.py -h <host> -p <port> -t <topic> -m <message>')
            sys.exit(-1)
        for n in range(0, 10):
            power_on(power_key)
            # Try until the device is connected
            while (True):
                try:
                    ser = serial.Serial('/dev/ttyUSB3',9600,timeout=1) # lower right usb port on RPI4
                except Exception as e:
                    continue
                break
            checkStart(10) # Wait until the device is started
            ser = serial.Serial('/dev/ttyUSB3',9600,timeout=1) # lower right usb port on RPI4
            ser.flushInput()
            sys.argv[8] = str(n)
            main(sys.argv[1:])
            power_down(power_key)
            ser.close()
            
    except Exception as e:
        print(e)
        if ser != None:
            ser.close()
            power_down(power_key)
            GPIO.cleanup()
