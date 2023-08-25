import serial
import RPi.GPIO as GPIO
import time
import sys

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
def checkStart(timeout, radio):
    print('Checking if simcom started')
    # loop until response
    radio.write( 'AT\r\n'.encode() )
    while True:
        timeout -= 1
        time.sleep(1)
        if radio.in_waiting != 0:
            recBuff = radio.read(radio.in_waiting)
            print('SOM7080G responded: ' + recBuff.decode())
            if 'OK' in recBuff.decode():
                recBuff = ''
                break 
        if timeout == 0:
            print('timed out at start')
            break
    
# send AT command to simcom
# command: AT command   timeout: timeout for answer, if 0 wait infinite amount of time
def send_command(command, timeout, radio):
    radio.write((command + '\r\n' ).encode())
    rec_buff = ''
    while True:
        timeout -= 1
        time.sleep(0.1)
        if radio.in_waiting:
            time.sleep(0.01)
            rec_buff = rec_buff + radio.read(radio.in_waiting).decode()
        if timeout == 0:
            print('timed out')
            break
        if 'OK\r\n' in rec_buff or 'ERROR\r\n' in rec_buff:
            break
    print('Response: ' + rec_buff)

def conn_mqtt(host, port):
    # Establish connection and send message
    print('Select LTE mode')
    send_command('AT+CNMP=38', 10, radio)
    print('Activate network bearing')
    send_command('AT+CNACT=0,1', 10, radio)
    print('Set TCP index')
    send_command('AT+CACID=0', 10, radio)
    
    print('Set broker')
    send_command('AT+SMCONF=\"URL\",\"' + host + '\",\"' + str(port) + '\"', 10, radio)
    print('Set keeptime')
    send_command('AT+SMCONF=\"KEEPTIME\",60', 10, radio)
    print('Set cleanss')
    send_command('AT+SMCONF=\"CLEANSS\",1', 10, radio)
    
    print('Connect to server')
    send_command('AT+SMCONN', 300, radio)

def pub_mqtt(topic, message):
    print('Send packet: ' + message)
    #send_command(('AT+SMPUB=\"' + topic + '\",' + str(len(message)) + ',1,1\r\n' + message), 30, radio)
    radio.write(('AT+SMPUB=\"' + topic + '\",' + str(len(message)) + ',1,1\r\n').encode())
    time.sleep(0.1)
    send_command(message, 30, radio)
    
    
def disconn_mqtt():
    print('Disconnect')
    send_command('AT+SMDISC', 10, radio)

if __name__ == "__main__":

	sensor = serial.Serial(
		port='/dev/ttyS0',
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1
	)
	
	#power_on(power_key)

	power_on(power_key)
    
	radio = serial.Serial(
	    '/dev/ttyUSB3',
	    9600,
	    timeout=1
	) # lower right usb port on RPI4 # needs to be global, kind of ugly :/
    
	radio.flushInput()
	checkStart(10, radio)
	
	conn_mqtt('broker.ssvl.kth.se', 1883)

	while (True):
		line_encoded = sensor.readline()
		line = line_encoded.decode()
		words = line.split()
	
		if (len(words) < 1):
			continue

		if (words[0] == 'send'):
			if (len(words) > 3):
				command = words[0]
				topic = words[1]
				message = words[2]
				length = words[3]
				pub_mqtt(topic, message)
			else:
				print('Too few arguments Usage:')
		elif (words[0] == 'loop'):
			if (len(words) > 1):
				command = words[0]
				topic = words[1]
				amount = int(words[2])
				sleeptime = int(words[3])
				for i in range(0, 100):
				    pub_mqtt(topic, str(i))
				    time.sleep(sleeptime)
			else:
				print('Too few arguments Usage:')
		elif (words[0] == 'z'):
		    break
		else:
			print('Unknown commad')
	disconn_mqtt()
	power_down(power_key)
