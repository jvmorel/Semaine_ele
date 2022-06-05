# Complete project details at https://RandomNerdTutorials.com
import usocket as socket
import uselect as select
from machine import Pin, PWM
  
import time
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

client_id = ubinascii.hexlify(machine.unique_id())
station = None
#...AP mode
boot_button = Pin(0, Pin.IN)

#...Sation mode
print('Station mode')
ssid = 'Olympie'
password = 'maisonambilly'
#ssid = 'Semaine_ele'
#password = 'Montbrillant'
station = network.WLAN(network.STA_IF)
station.active(True)
station.ifconfig(('192.168.0.40', '255.255.255.0', '192.168.0.254', '192.168.0.254'))
#station.ifconfig(('192.168.4.5', '255.255.255.0', '192.168.0.254', '192.168.4.1'))
station.connect(ssid, password)
while station.isconnected() == False:
  pass
print('Connection successful')
print(station.ifconfig())

    
