##############################################################################################################
#
#
#
#
##############################################################################################################
##  Importation des librairies                                                                              ##
##############################################################################################################
#
#
#
##############################################################################################################
from machine import ADC
from machine import SoftI2C
from machine import Pin, PWM
import random
import _thread
import tm1637 
import usocket as socket
import uselect as select
import time
from hcsr04 import HCSR04
from bmp180 import BMP180
import onewire
import ds18x20
import re
import gc
gc.collect()
import usocket as socket
import uselect as select
##############################################################################################################
#...Dictionnaire pour stocker les valeurs des capteurs
valeurs = {}
#
#
#
#
##############################################################################################################
##  Fonctions pour le serveur WEB                                                                           ##
##############################################################################################################
#
#
#
##############################################################################################################
#...Pour envoyer la page html
##############################################################################################################
def send_web_page(conn):
  html  = """<html>  """
  html += """      <head>  """
  html += """      <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>  """
  html += """      <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">  """
  html += """      <link rel="preconnect" href="https://fonts.googleapis.com">  """
  html += """      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>  """
  html += """      <link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">  """
  html += """      <title>Station météo </title>  """
  html += """      <meta name="viewport" content="width=device-width, initial-scale=1">  """
  html += """      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />  """
  html += """      <meta http-equiv="refresh" content="5" >  """
  html += """      <link rel="icon" href="data:,">  """
  conn.sendall(html)

  ###############################################################
  #...Definition du style
  ###############################################################
  html  = """  """
  html += """      <style>  """
  html += """          body{  """
  html += """              background-color: rgba(232, 222, 209, 0.3);  """
  html += """              font-family: 'Lato', sans-serif;  """
  html += """              width:75%;  """
  html += """              margin: auto;  """
  html += """              text-align: center;  """
  html += """          }  """
  html += """  """
  html += """          p{  """
  html += """              font-size: 1.5rem;  """
  html += """  """
  html += """          }  """
  html += """  """
  html += """          h1, h2, h3, h4, h5, h6{  """
  html += """              font-family: 'Montserrat', sans-serif;  """
  html += """              text-transform: uppercase;  """
  html += """              letter-spacing: .3rem;  """
  html += """          }  """
  html += """  """
  html += """          h1{  """
  html += """              color: #0F3376;  """
  html += """              margin-top: 5%;  """
  html += """              font-size: 3rem;  """
  html += """          }  """
  html += """  """
  html += """          h2{  """
  html += """              font-size: 2rem;  """
  html += """          }  """
  html += """  """
  html += """          /*  """
  html += """          table{  """
  html += """          font-size: 2rem;  """
  html += """          text-align:left;  """
  html += """          }  """
  html += """          */  """
  html += """  """
  html += """          .insideBox{  """
  html += """              margin:auto;  """
  html += """              width=75%;  """
  html += """              background-color: #fff;  """
  html += """              padding:5%;  """
  html += """              margin-bottom: 5%;  """
  html += """              text-align: center;  """
  html += """          }  """
  html += """  """
  html += """          button{  """
  html += """              display: inline-block;  """
  html += """              border: none;  """
  html += """              border-radius: 4px;  """
  html += """              margin: 2px;  """
  html += """              padding: 16px 40px;  """
  html += """              font-size: 30px;  """
  html += """              color: white;  """
  html += """              cursor: pointer;  """
  html += """          }  """
  html += """  """
  html += """          .button{  """
  html += """              background-color: #e7bd3b;  """
  html += """          }  """
  html += """  """
  html += """          .button2{  """
  html += """              background-color: #4286f4;  """
  html += """          }  """
  html += """  """
  html += """          .grid-container {  """
  html += """              display: grid;  """
  html += """              grid-template-columns: 1fr 1fr;  """
  html += """              grid-gap: 1%;  """
  html += """              margin-bottom: 5%;  """
  html += """          }  """
  html += """            """
  html += """          .grid-container-3 {  """
  html += """              display: grid;  """
  html += """              grid-template-columns: 1fr 1fr 1fr;  """
  html += """              grid-gap: 1%;  """
  html += """              margin-bottom: 5%;  """
  html += """          }  """
  html += """  """
  html += """          .grid-container-4 {  """
  html += """              display: grid;  """
  html += """              grid-template-columns: 1fr 1fr 1fr 1fr;  """
  html += """              grid-gap: 1%;  """
  html += """              margin-bottom: 5%;  """
  html += """          }  """
  html += """  """
  html += """          .iconIndicator{  """
  html += """              font-size: 3rem;  """
  html += """          }  """
  html += """  """
  html += """      </style>  """
  html += """  </head>  """
  html += """  <body>  """
  html += """  """
  conn.sendall(html)
  
  ###############################################################
  #...Affichage du titre
  ###############################################################
  html  = """  """
  html += """<!--  """
  html += """<div class="outsideBox">  """
  html += """-->  """
  html += """      <h1><i class="fas fa-cloud-sun"></i> MontMétéo <i class="fas fa-cloud-rain"></i></h1>  """
  html += """      <h2>Station météo personnelle</h2>  """
  html += """  """
  conn.sendall(html)

  ###############################################################
  html  = """  """
  html += """      <div class="insideBox">  """
  html += """          <h3>Données atmosphériques</h3>  """
  html += """          <div class="grid-container-3">  """
  conn.sendall(html)

  ###############################################################
  #...Affichage de la lumiere
  ###############################################################
  html  = """  """
  html += """              <div>  """
  #... Cas 1
  if valeurs['lumiere'] == 1 : 
    html += """                  <i class="fas fa-moon iconIndicator"></i><p>Il fait nuit.</p>  """
  #... Cas 2
  else:
    html += """                  <i class="fas fa-sun iconIndicator"></i><p>Il fait jour.</p>  """
  #... fin cas
  html += """              </div>  """
  conn.sendall(html)

  ###############################################################
  #...Affichage de la sonde de température
  ###############################################################
  html  = """  """
  html += """              <div>  """
  html += """                  <p>  """
  #... Cas 1
  if valeurs['temperature'] > 30 : 
    html += """                      <i class="fas fa-thermometer-full " style="color: #DC143C;font-size: 4rem;"></i>  """
    html += """                      <br>  """
  #... Cas 2
  elif valeurs['temperature'] >20:
    html += """                      <i class="fas fa-thermometer-half" style="color: #2ECC71;font-size: 4rem;"></i>  """
    html += """                      <br>  """
  #... Cas 3
  else:
    html += """                      <i class="fas fa-thermometer-quarter" style="color: #85C1E9;font-size: 4rem;"></i>  """
    html += """                      <br>  """
  #... fin cas
  html += """                      <span style="font-size: 7rem">%d</span>  """ % (valeurs['temperature'])
  html += """                      <span style="vertical-align: top;">°C</span>  """
  html += """                  </p>  """
  html += """              </div>  """
  conn.sendall(html)

  ###############################################################
  #...Affichage de la sonde température / pression / altitude
  ###############################################################
  html  = """  """
  html += """              <div>  """
  html += """                  <h4>Sonde</h4>  """
  html += """                  <p><i class="fas fa-thermometer-half"></i><br> %d °C</p>  """%(valeurs['temperature_bmp180'])
  html += """                  <p><i class="fas fa-weight-hanging"></i><br> %d hPa</p>  """%(valeurs['pression_bmp180'])
  html += """                  <p><i class="fas fa-mountain"></i><br> %d m</p>  """%(valeurs['altitude_bmp180'])
  html += """              </div>  """
  html += """  """
  conn.sendall(html)


  ###############################################################
  html  = """  """
  html += """          </div>  """
  html += """      </div>  """
  html += """  """
  conn.sendall(html)

  ###############################################################
  #...Controle des led depuis la page WEB
  ###############################################################
  html  = """  """
  html += """      <div class="grid-container-4">  """
  html += """          <div class="insideBox">  """
  html += """              <h3>LED Blanche</h3>  """
  html += """              <p>   """
  html += """                  <i class="fas fa-lightbulb" style="color:#FFD700;"></i>  """
  html += """                  <br><br>  """
  html += """                  <a href="/?led_blanche=on"><button class="button">ON</button></a>  """
  html += """              </p>  """
  html += """              <p>             """
  html += """                  <i class="fas fa-lightbulb" style="color:#dcdcdc;"></i>  """
  html += """                  <br><br>  """
  html += """                  <a href="/?led_blanche=off"><button class="button2">OFF</button></a>  """
  html += """              </p>  """
  html += """          </div>  """
  html += """          <div class="insideBox">  """
  html += """              <h3>LED Bleue </h3>  """
  html += """              <p>   """
  html += """                  <i class="fas fa-lightbulb" style="color:#FFD700;"></i>  """
  html += """                  <br><br>  """
  html += """                  <a href="/?led_bleue=on"><button class="button">ON</button></a>  """
  html += """              </p>  """
  html += """              <p>             """
  html += """                  <i class="fas fa-lightbulb" style="color:#dcdcdc;"></i>  """
  html += """                  <br><br>  """
  html += """                  <a href="/?led_bleue=off"><button class="button2">OFF</button></a>  """
  html += """              </p>  """
  html += """          </div>  """
  html += """          <div class="insideBox">  """
  html += """              <h3>LED Rouge </h3>  """
  html += """              <p>   """
  html += """                  <i class="fas fa-lightbulb" style="color:#FFD700;"></i>  """
  html += """                  <br><br>  """
  html += """                  <a href="/?led_rouge=on"><button class="button">ON</button></a>  """
  html += """              </p>  """
  html += """              <p>             """
  html += """                  <i class="fas fa-lightbulb" style="color:#dcdcdc;"></i>  """
  html += """                  <br><br>  """
  html += """                  <a href="/?led_rouge=off"><button class="button2">OFF</button></a>  """
  html += """              </p>  """
  html += """          </div>  """
  conn.sendall(html)

  ###############################################################
  #...Controle du buzzer depuis la page WEB
  ###############################################################
  html  = """  """
  html += """          <div class="insideBox">  """
  html += """              <p>  """
  html += """              <h3>Buzzer </h3>  """
  html += """              <p>  """
  html += """                  <i class="fas fa-bullhorn" style="color:#FF6347;"></i>  """
  html += """                  <br><br>  """
  html += """                  <a href="/?buz=on"><button class="button">ON</button></a>  """
  html += """              </p>  """
  html += """              <p>  """
  html += """                  <i class="fas fa-bullhorn" style="color:#dcdcdc;"></i>  """
  html += """                  <br><br>  """
  html += """                  <a href="/?buz=off"><button class="button2">OFF</button></a>  """
  html += """              </p>  """
  html += """          </div>  """
  conn.sendall(html)

  ###############################################################
  html  = """  """
  html += """      </div>  """
  html += """  """
  conn.sendall(html)
  

  ###############################################################
  #...Affichage du capteur d'obstacle
  ###############################################################
  html  = """  """
  html += """      <div class="insideBox">  """
  html += """          <h3>Détection</h3>  """
  html += """          <div class="grid-container-3">  """
  html += """              <div>  """
  #... Cas 1
  if  valeurs['obstacle'] == 0 : 
    html += """                  <i class="fas fa-exclamation iconIndicator"></i>   """
    html += """                  <p>Quelque chose est situé devant le détecteur.</p>  """
  #... Cas 2
  else:
    html += """                  <i class="fas fa-times iconIndicator"></i>  """
    html += """                  <p>Il n'y a rien devant le détecteur.</p>  """
  #... fin cas
  html += """  """
  html += """              </div>  """
  conn.sendall(html)
  
  ###############################################################
  #...Affichage de l'état du bouton
  ###############################################################
  html  = """  """
  html += """              <div>  """
  #... Cas 1
  if valeurs['bouton'] == 1: 
    html += """                  <i class="fas fa-exclamation iconIndicator"></i>   """
    html += """                  <p>Le bouton est appuyé.</p>  """
  #... Cas 2
  else:
    html += """                  <i class="fas fa-times iconIndicator"></i>  """
    html += """                  <p>Le bouton n'est pas appuyé.</p>  """
  #... fin cas
  html += """  """
  html += """              </div>  """
  conn.sendall(html)

  ###############################################################
  #...Affichage du détecteur de mouvement
  ###############################################################
  html  = """  """
  html += """              <div>  """
  #... Cas 1
  if valeurs['mouvement'] == 1: 
    html += """                  <i class="fas fa-exclamation iconIndicator"></i>   """
    html += """                  <p>Mouvement détecté.</p>  """
  #... Cas 2
  else:
    html += """                  <i class="fas fa-times iconIndicator"></i>  """
    html += """                  <p>Il n'y a pas de mouvement.</p>  """
  #... fin cas
  html += """  """
  html += """              </div>  """
  conn.sendall(html)

  ###############################################################
  #...fin
  ###############################################################
  html  = """  """
  html += """          </div>  """
  html += """      </div>  """
  html += """  """
  html += """  </body>  """
  html += """</html>  """
  html += """  """
  conn.sendall(html)
  return


##############################################################################################################
#...Pour gerer les requestes
##############################################################################################################
def client_handler(client_obj)client_handler(client_obj):
  
  poller = select.poll()
  poller.register(client_obj, select.POLLIN)
  res = poller.poll(1000)  # time in milliseconds
  if not res:
      return
  request = client_obj.recv(1024)
  request = str(request)

  if request.find('/?led_blanche=on') == 6:
    led_blanche.value(1)
  if request.find('/?led_blanche=off') == 6:
    led_blanche.value(0)
  
  if request.find('/?led_bleue=on') == 6:
    led_bleue.value(1)
  if request.find('/?led_bleue=off') == 6:
    led_bleue.value(0)
  
  if request.find('/?led_rouge=on') == 6:
    led_rouge.value(1)
  if request.find('/?led_rouge=off') == 6:
    led_rouge.value(0)
  
  if request.find('/?buz=on')  > 0:
    buzzer.value(1)
  if request.find('/?buz=off') > 0:
    buzzer.value(0)
  
  #...Response
  client_obj.send('HTTP/1.1 200 OK\n')
  client_obj.send('Content-Type: text/html\n')
  client_obj.send('Connection: close\n\n')
  Read_FastSensors()
  send_web_page(client_obj)
  
  return

##############################################################################################################
#...Pour attendre les requetes HTML
##############################################################################################################
def Serveur_web_Thread():
  data_interval = 0.5 #...Time in sec between measurment
  while True:

    #...Request
    r, w, err = select.select((s,), (), (), data_interval)
    for readable in r:
      conn, addr = s.accept()
      print('Got a connection from %s' % str(addr))
      try:
        client_handler(conn)
        conn.close()
      except OSError as e:
        pass

##############################################################################################################
#
#
#
#
##############################################################################################################
##  Définition des capteurs et initialisation des valeurs                                                   ##
##############################################################################################################
#
#
##############################################################################################################
#...LED  
global led_rouge
global led_blanche
global led_bleue
led_rouge   = Pin(2, Pin.OUT)
led_blanche = Pin(23, Pin.OUT)
led_bleue   = Pin(17, Pin.OUT)
#led_rouge.value(1) allume, led_rouge.value(0) eteind
##############################################################################################################
#...Buzzer
global buzzer
buzzer = Pin(19, Pin.OUT)
     # buzzer.value(1) allume, buzzer.value(0) eteind
#frequency = 4000
#buzzer = PWM(Pin(19), frequency)
#buzzer.duty(0)


##############################################################################################################
#...TM1637           | écran 7-Segment à 4 Chiffres 
global tm
tm= tm1637.TM1637(clk=Pin(15), dio=Pin(4))
tm.show('    ')
     # tm.show('10') #display the number 10 on the display


     
##############################################################################################################
#...                 | Module numérique de capteur d'intensité lumineuse
global lumiere
lumiere= Pin(35, Pin.IN, Pin.PULL_DOWN)
     # valeurs['lumiere'] = lumiere.value() # 0 si lumiere, 1 sinon.

##############################################################################################################
#...                 | Module numérique de capteur d'intensité lumineuse
global bouton
bouton= Pin(16, Pin.IN, Pin.PULL_DOWN)
     # valeurs['bouton'] = bouton.value() # 1 si bouton, 0 sinon.

##############################################################################################################
#...                 | IR Module Infrarouge de Capteur D'évitement D'obstacle 
global obstacle
obstacle = Pin(27, Pin.IN, Pin.PULL_DOWN)
     # valeurs['obstacle'] = obstacle.value() # 0 si obstacle, 1 sinon.
     
##############################################################################################################
#...HCS-SR505        | Capteur de Mouvement Humain Infrarouge                     
global mouvement
mouvement = Pin(14, Pin.IN, Pin.PULL_DOWN)
     # valeurs['mouvement'] = mouvement.value() # 0 si lumiere, 1 sinon.



##############################################################################################################
#...BMP180           | capteur de température de Pression barométrique 
#global bus
#global bmp180
#bus =  SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)   # on esp32
#bmp180= BMP180(bus)
#bmp180.oversample_sett = 2
#bmp180.baseline = 101325
valeurs['temperature_bmp180'] = 0
valeurs['pression_bmp180']    = 0
valeurs['altitude_bmp180']    = 0
     # valeurs['temperature_bmp180'] = bmp180.temperature
     # valeurs['pression_bmp180'] = bmp180.pressure
     # valeurs['altitude_bmp180'] = bmp180.altitude

##############################################################################################################
#...DS18B20          | kit capteur de température
ow= onewire.OneWire(Pin(5))
sonde_temp= ds18x20.DS18X20(ow)
roms= sonde_temp.scan()
valeurs['temperature'] = 0
     # sonde_temp.convert_temp()
     # time.sleep(0.75)
     # valeurs['temperature'] = sonde_temp.read_temp(roms[0])


##############################################################################################################
#...HC-SR04          | Module Ultrason de Capteur de Distance 
capteur_distance = HCSR04(trigger_pin=13, echo_pin=12,echo_timeout_us=50000)
     # valeurs['distance'] = capteur_distance.distance_cm()

##############################################################################################################
#...KY-038           | Capteur de Son 
son_analog= ADC(Pin(36))
#son_analog.atten(ADC.ATTN_11DB)       # Full range: 3.3v
son_analog.width(ADC.WIDTH_9BIT)     # Range 0 to 4095
bruit= Pin(0, Pin.IN, Pin.PULL_DOWN)
     # valeurs['son_analog']  =  son_analog.read()
     # valeurs['bruit'] =  bruit.value() # 1 si son, 0 sinon.
def volume_sonore(a):
  import math
  v0 = 31
  #...retourne le volume sonor en decibel
  return 20*math.log10(a/v0)

##############################################################################################################
#
#
#
##############################################################################################################
##  Fonction pour stocker les valeurs des capteurs dans la variable valeurs                                 ##
##############################################################################################################
#
##############################################################################################################
def Read_FastSensors():
  valeurs['obstacle']    = obstacle.value() # 0 si obstacle, 1 sinon.
  valeurs['lumiere']     = lumiere.value()
  valeurs['bouton']      = bouton.value() # 1 si bouton, 0 sinon.
  valeurs['mouvement']   = mouvement.value() # 0 si lumiere, 1 sinon.
 

##############################################################################################################
def Read_SlowSensors_Thread():
  while True:
    time.sleep(3)
    try:
      sonde_temp.convert_temp()
      time.sleep(0.9)
      valeurs['temperature'] = sonde_temp.read_temp(roms[0])
    except OSError as e:
      print('Probleme avec la sonde de temperature')
      pass

    try:
      valeurs['temperature_bmp180'] = 14.678
      valeurs['pression_bmp180']    = 101500
      valeurs['altitude_bmp180']    = 350
    except OSError as e:
      print('Probleme avec la sonde de pression bmp180')
      pass

##############################################################################################################
def Onbord_Thread():
  while True:
#    time.sleep(20)
    tm.temperature(int(valeurs['temperature']))
#    for led in [led_rouge, led_blanche, led_bleue]:
    for led in [led_rouge, led_blanche]:
      i = random.randint(1,6)
      led_blanche.value(1)
      time.sleep(0.1*i)
      led_blanche.value(0)
      i = random.randint(1,6)
      time.sleep(0.1*i)
 
##############################################################################################################
##  Initialisation du serveur web                                                                           ##
##############################################################################################################
#
#
##############################################################################################################
global time_Start
global conn
global s
time_Start= time.ticks_ms()
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn=  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(None)
#s.setblocking(0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)
for led in [led_rouge]:
  led_blanche.value(1)
  time.sleep(0.2)
  led_blanche.value(0)
  time.sleep(0.2)
  led_blanche.value(1)
  time.sleep(0.2)
  led_blanche.value(0)
  time.sleep(0.2)
  led_blanche.value(1) 
  time.sleep(0.2)
  led_blanche.value(0)
_thread.start_new_thread(Read_SlowSensors_Thread, ())
time.sleep(0.5)
_thread.start_new_thread(Serveur_web_Thread, ())
#time.sleep(0.5)
#_thread.start_new_thread(Onbord_Thread, ())

##############################################################################################################
#
#
#
#
##############################################################################################################
##  Boucle pincipale                                                                                        ##
##############################################################################################################
#
#
##############################################################################################################

