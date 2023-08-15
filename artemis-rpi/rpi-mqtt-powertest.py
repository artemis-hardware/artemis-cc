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
    time.sleep(2)
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(power_key,GPIO.LOW)
    time.sleep(5)
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
    time.sleep(5)
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
    print('Response: ' + rec_buff.decode())

def send_mqtt(host, port, topic, message):
    # Testing things
    print('Test simcard')
    send_command('AT+CPIN?', 5)
    print('Check network status')
    send_command('AT+CGREG?', 5)
    print('Test simcard')
    send_command('AT+CPIN?', 3)
    print('Test signal strength')
    send_command('AT+CSQ', 3)
    print('Request UE system info')
    send_command('AT+CPSI?', 3)
    print('Check network status')
    send_command('AT+CGREG?', 3)
    
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
    power_down(power_key)

def testloop:
    msg = 1
    host = broker.ssvl.kth.se
    port = 1883
    topic = artemis_test
    for i in 0..100:
        print('sending: ' + msg)
        send_mqtt(host, port, topic, msg)
        print(sent)
        wait(1000)
        
if __name__ == "__main__":
    try:
        power_on(power_key)
        ser = serial.Serial('/dev/ttyUSB3',9600,timeout=1) # lower right usb port on RPI4
        ser.flushInput()
        checkStart(10)
        testloop()
        
    except Exception as e:
        print(e)
        if ser != None:
            ser.close()
            power_down(power_key)
            GPIO.cleanup()
