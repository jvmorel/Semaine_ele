##############################################################################################################
#
#  !!!! Modification par rapport à ce qui a été fait en classe
#
#  Utilisation des F-string pour écrire la température dans les lignes.
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
