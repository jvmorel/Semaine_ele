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
  html  = """<html>
        <head>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
        <title>Station météo </title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <meta http-equiv="refresh" content="5" >
        <link rel="icon" href="data:,">
  """
  conn.sendall(html)

  ###############################################################
  #...Definition du style
  ###############################################################
  html  = """
        <style>
            body{
                background-color: rgba(232, 222, 209, 0.3);
                font-family: 'Lato', sans-serif;
                width:75%;
                margin: auto;
                text-align: center;
            }
  
            p{
                font-size: 1.5rem;
  
            }
  
            h1, h2, h3, h4, h5, h6{
                font-family: 'Montserrat', sans-serif;
                text-transform: uppercase;
                letter-spacing: .3rem;
            }
  
            h1{
                color: #0F3376;
                margin-top: 5%;
                font-size: 3rem;
            }
  
            h2{
                font-size: 2rem;
            }
  
            /*
            table{
            font-size: 2rem;
            text-align:left;
            }
            */
  
            .insideBox{
                margin:auto;
                width=75%;
                background-color: #fff;
                padding:5%;
                margin-bottom: 5%;
                text-align: center;
            }
  
            button{
                display: inline-block;
                border: none;
                border-radius: 4px;
                margin: 2px;
                padding: 16px 40px;
                font-size: 30px;
                color: white;
                cursor: pointer;
            }
  
            .button{
                background-color: #e7bd3b;
            }
  
            .button2{
                background-color: #4286f4;
            }
  
            .grid-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                grid-gap: 1%;
                margin-bottom: 5%;
            }
            
            .grid-container-3 {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                grid-gap: 1%;
                margin-bottom: 5%;
            }
  
            .grid-container-4 {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr 1fr;
                grid-gap: 1%;
                margin-bottom: 5%;
            }
  
            .iconIndicator{
                font-size: 3rem;
            }
  
        </style>
    </head>
    <body>
  """
  conn.sendall(html)
  
  ###############################################################
  #...Affichage du titre
  ###############################################################
  html  = """
  <!--
  <div class="outsideBox">
  -->
        <h1><i class="fas fa-cloud-sun"></i> MontMétéo <i class="fas fa-cloud-rain"></i></h1>
        <h2>Station météo personnelle</h2>
  """
  conn.sendall(html)

  ###############################################################
  html  = """
        <div class="insideBox">
            <h3>Données atmosphériques</h3>
            <div class="grid-container-3">
  """
  conn.sendall(html)

  ###############################################################
  #...Affichage de la lumiere
  ###############################################################
  html  = """ <div>  """
  #... Cas 1
  if valeurs['lumiere'] == 1 : 
    html += """ <i class="fas fa-moon iconIndicator"></i><p>Il fait nuit.</p> """
  #... Cas 2
  else:
    html += """ <i class="fas fa-sun iconIndicator"></i><p>Il fait jour.</p> """
  #... fin cas
  html += """ </div>  """
  conn.sendall(html)

  ###############################################################
  #...Affichage de la sonde de température
  ###############################################################
  html  = """
   <div>
   <p>
  """
  #... Cas 1
  if valeurs['temperature'] > 30 : 
    html += """<i class="fas fa-thermometer-full " style="color: #DC143C;font-size: 4rem;"></i>  <br>"""
  #... Cas 2
  elif valeurs['temperature'] >20:
    html += """<i class="fas fa-thermometer-half" style="color: #2ECC71;font-size: 4rem;"></i>  <br>"""
  #... Cas 3
  else:
    html += """<i class="fas fa-thermometer-quarter" style="color: #85C1E9;font-size: 4rem;"></i>  <br>"""
  #... fin cas
  html += f"""
  <span style="font-size: 7rem">{valeurs['temperature']:0.0f}</span>
  <span style="vertical-align: top;">°C</span>
  </p>
  </div>
  """
  conn.sendall(html)

  ###############################################################
  #...Affichage de la sonde température / pression / altitude
  ###############################################################
  html  = f"""
  <div>
  <h4>Sonde</h4>
  <p><i class="fas fa-thermometer-half"></i><br> {valeurs['temperature_bmp180']:0.0f} °C</p>
  <p><i class="fas fa-weight-hanging"></i><br> {valeurs['pression_bmp180']/100:0.0f} hPa</p>
  <p><i class="fas fa-mountain"></i><br> {valeurs['altitude_bmp180']:0.0f} m</p>
  </div>
  """
  conn.sendall(html)


  ###############################################################
  html  = """
            </div>
        </div>
  """
  conn.sendall(html)

  ###############################################################
  #...Controle des led depuis la page WEB
  ###############################################################
  html  = """
        <div class="grid-container-4">
            <div class="insideBox">
                <h3>LED Blanche</h3>
                <p> 
                    <i class="fas fa-lightbulb" style="color:#FFD700;"></i>
                    <br><br>
                    <a href="/?led_blanche=on"><button class="button">ON</button></a>
                </p>
                <p>           
                    <i class="fas fa-lightbulb" style="color:#dcdcdc;"></i>
                    <br><br>
                    <a href="/?led_blanche=off"><button class="button2">OFF</button></a>
                </p>
            </div>
            <div class="insideBox">
                <h3>LED Bleue </h3>
                <p> 
                    <i class="fas fa-lightbulb" style="color:#FFD700;"></i>
                    <br><br>
                    <a href="/?led_bleue=on"><button class="button">ON</button></a>
                </p>
                <p>           
                    <i class="fas fa-lightbulb" style="color:#dcdcdc;"></i>
                    <br><br>
                    <a href="/?led_bleue=off"><button class="button2">OFF</button></a>
                </p>
            </div>
            <div class="insideBox">
                <h3>LED Rouge </h3>
                <p> 
                    <i class="fas fa-lightbulb" style="color:#FFD700;"></i>
                    <br><br>
                    <a href="/?led_rouge=on"><button class="button">ON</button></a>
                </p>
                <p>           
                    <i class="fas fa-lightbulb" style="color:#dcdcdc;"></i>
                    <br><br>
                    <a href="/?led_rouge=off"><button class="button2">OFF</button></a>
                </p>
            </div>
  """
  conn.sendall(html)

  ###############################################################
  #...Controle du buzzer depuis la page WEB
  ###############################################################
  html  = """
            <div class="insideBox">
                <p>
                <h3>Buzzer </h3>
                <p>
                    <i class="fas fa-bullhorn" style="color:#FF6347;"></i>
                    <br><br>
                    <a href="/?buz=on"><button class="button">ON</button></a>
                </p>
                <p>
                    <i class="fas fa-bullhorn" style="color:#dcdcdc;"></i>
                    <br><br>
                    <a href="/?buz=off"><button class="button2">OFF</button></a>
                </p>
            </div>
  """
  conn.sendall(html)

  ###############################################################
  html  = """
  </div>
  """
  conn.sendall(html)
  

  ###############################################################
  #...Affichage du capteur d'obstacle
  ###############################################################
  html  = """
        <div class="insideBox">
            <h3>Détection</h3>
            <div class="grid-container-3">
                <div>
  """
  #... Cas 1
  if  valeurs['obstacle'] == 0 : 
    html += """ <i class="fas fa-exclamation iconIndicator"></i> 
                <p>Quelque chose est situé devant le détecteur.</p>
            """
  #... Cas 2
  else:
    html += """ <i class="fas fa-times iconIndicator"></i>
                <p>Il n'y a rien devant le détecteur.</p>
            """
  #... fin cas
  
  html += """ 
  </div>
  """
  conn.sendall(html)
  
  ###############################################################
  #...Affichage de l'état du bouton
  ###############################################################
  html  = """
                <div>
            """
  #... Cas 1
  if valeurs['bouton'] == 1: 
    html += """ <i class="fas fa-exclamation iconIndicator"></i> 
                <p>Le bouton est appuyé.</p>
            """
  #... Cas 2
  else:
    html += """ <i class="fas fa-times iconIndicator"></i>
                <p>Le bouton n'est pas appuyé.</p>
            """
  #... fin cas
  html += """ 
  </div>
  """
  conn.sendall(html)

  ###############################################################
  #...Affichage du détecteur de mouvement
  ###############################################################
  html  = """
                <div>
            """
  #... Cas 1
  if valeurs['mouvement'] == 1: 
    html += """ <i class="fas fa-exclamation iconIndicator"></i> 
                <p>Mouvement détecté.</p>
    """
  #... Cas 2
  else:
    html += """ <i class="fas fa-times iconIndicator"></i>
                <p>Il n'y a pas de mouvement.</p>
    """
  #... fin cas
  html += """ 
  </div>
  """
  conn.sendall(html)

  ###############################################################
  #...fin
  ###############################################################
  html  = """
            </div>
        </div>
  
    </body>
  </html>
  """
  conn.sendall(html)
  return


##############################################################################################################
#...Pour gerer les requestes
##############################################################################################################
def client_handler(client_obj):
  
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
led_rouge   = Pin(2, Pin.OUT)
led_blanche = Pin(23, Pin.OUT)
led_bleue   = Pin(17, Pin.OUT)
     #led_rouge.value(1) allume, led_rouge.value(0) eteind
##############################################################################################################
#...Buzzer
buzzer = Pin(19, Pin.OUT)
     # buzzer.value(1) allume, buzzer.value(0) eteind


##############################################################################################################
#...TM1637           | écran 7-Segment à 4 Chiffres 
tm= tm1637.TM1637(clk=Pin(15), dio=Pin(4))
tm.show('    ')
     # tm.show('10') #display the number 10 on the display


     
##############################################################################################################
#...                 | Module numérique de capteur d'intensité lumineuse
lumiere= Pin(35, Pin.IN, Pin.PULL_DOWN)
     # valeurs['lumiere'] = lumiere.value() # 0 si lumiere, 1 sinon.

##############################################################################################################
#...                 | Module numérique de capteur d'intensité lumineuse
bouton= Pin(16, Pin.IN, Pin.PULL_DOWN)
     # valeurs['bouton'] = bouton.value() # 1 si bouton, 0 sinon.

##############################################################################################################
#...                 | IR Module Infrarouge de Capteur D'évitement D'obstacle 
obstacle = Pin(27, Pin.IN, Pin.PULL_DOWN)
     # valeurs['obstacle'] = obstacle.value() # 0 si obstacle, 1 sinon.
     
##############################################################################################################
#...HCS-SR505        | Capteur de Mouvement Humain Infrarouge                     
mouvement = Pin(14, Pin.IN, Pin.PULL_DOWN)
     # valeurs['mouvement'] = mouvement.value() # 0 si lumiere, 1 sinon.



##############################################################################################################
#...BMP180           | capteur de température de Pression barométrique 
bus =  SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)   # on esp32
bmp180= BMP180(bus)
bmp180.oversample_sett = 2
bmp180.baseline = 101325
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
valeurs['temperature'] = 0
     # roms= sonde_temp.scan()
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
    try:
      roms= sonde_temp.scan()
      if len(roms)>0 :
        print(roms)
        sonde_temp.convert_temp()
        time.sleep(1)
        valeurs['temperature'] = sonde_temp.read_temp(roms[0])
      else:
        print("pas de roms")

      valeurs['temperature_bmp180'] = bmp180.temperature
      valeurs['pression_bmp180'] = bmp180.pressure
      valeurs['altitude_bmp180'] = bmp180.altitude
    except OSError as e:
      print('Probleme avec les sondes lentes')
      pass
    time.sleep(3)

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

