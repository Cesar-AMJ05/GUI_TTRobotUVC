# app.py 
# Servidor con Flask para la interfaz web del Modulo
# Se emplea Flask-SocketIO para la comunicación 
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import cv2 
import time
import threading

#Cargamos configuracion 
from config import Config

# Configuración inicial
app = Flask(__name__)
app.config.from_object(Config)


#Iniciamos SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=Config.ASYNC_MODE)

#Iniciamos rutas web
from routes.web_routes import register_web_routes
from routes.camara_routes import register_camera_routes

#Iniciamos servicios de camara
from services.camara_service import generate_frame, toggle_camera_visibility, get_camera_visibility
from services.camara_service import init_camera_service

#Iniciamos eventos de robot
from sockets.robot_events import register_robot_events
#Iniciamos eventos de notificaciones
from sockets.noti_events import noti_events
#Iniciamos eventos de datos del emisor
from sockets.data_events import register_data_emisor
#Iniciamos eventos de control
from sockets.control_events import register_conotrol_events

# Registro de rutas web
register_web_routes(app)
register_camera_routes(app)

#Iniciamos el servicio de la camara
init_camera_service()

# Registro de eventos de robot
register_robot_events(socketio)
# Registro de eventos de notificaciones
noti_events(socketio)
# Registro de eventos de datos del emisor
register_data_emisor(socketio)
#Registro de eventos de control
register_conotrol_events(socketio)


# Solicitud de datos a emisor
def request_emisor_data():
    while True:
        socketio.emit("solicitar-datos", {"request": "data"})
        time.sleep(15)  # cada 15 segundos
threading.Thread(target=request_emisor_data, daemon=True).start()





# Evitar debug=True mientras pruebas stream MJPEG
socketio.run(app, host='0.0.0.0', port=5000, debug=False)

