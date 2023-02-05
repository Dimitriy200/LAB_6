import RPi.GPIO as GPIO
from threading import Thread

import random
import time
from paho.mqtt import client as mqtt_client


broker = '192.168.1.226'
port = 1883
topic = "/DZ-IVT-360"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'DZ'
password = 'DZ'


# GPIO to LCD mapping
LCD_RS = 21 # Pi pin
LCD_RW = 26 # Pi pin
LCD_E  = 20 # Pi pin
LCD_D4 = 16 # Pi pin
LCD_D5 = 19 # Pi pin
LCD_D6 = 13 # Pi pin
LCD_D7 = 12 # Pi pin
 
# Device constants
LCD_CHR = True # Character mode
LCD_CMD = False # Command mode
LCD_WIDTH = 16    # Maximum characters per line

LCD_LINE_1 = 0x80 # LCD memory location for 1st line
LCD_LINE_2 = 0xC0 # LCD memory location 2nd line
 
# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

led1pin = 24
led2pin = 22
led3pin = 23
led4pin = 27

button1Pin = 6
button2Pin = 1
button3Pin = 7
button4Pin = 8



#CONNECT
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


#subscribe
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

#OUTPUT IN RASP
def lcd_text(message, line):
 # Send text to display
    message = message.ljust(LCD_WIDTH, '')
    lcd_write(line, LCD_CMD)
    for i in range(LCD_WIDTH):
      lcd_init()
    for i in range(line):
        lcd_write(ord(message[i]), LCD_CHR)


#GO



client = connect_mqtt()
subscribe(client)
client.loop_forever()
lcd_text(client.on_message)
