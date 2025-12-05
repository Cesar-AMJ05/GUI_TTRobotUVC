import socketio
import time
import atexit
import random

status_start = False
stop_robot = False
status_lamps = False
msg_lamps = "off"



# Crear cliente SocketIO
sio = socketio.Client(reconnection=True, reconnection_attempts=5, reconnection_delay=2)

# --- Eventos ---
@sio.event
def connect():
    print(" Conectado al servidor")
    sio.emit("is-online", {"status": "online", "success": True})

@sio.event
def disconnect():
    print("🔌 Me desconecté del servidor")

@sio.on("start-process")
def start_robot(data):
    global start_robot
    start_robot = not start_robot
    sio.emit("go-robot", {"status": "go", "success": start_robot})
    print("Iniciando proceso")
    #arduino.write(b'A')
    #arduino.flush()

@sio.on("go-home")
def go_home(data):
    sio.emit("go-home", {"status": "home", "success": True })
    print("Regresando a casa")


@sio.on("toggle-LampsUVC")
def toggle_lamps(data):
    global status_lamps, msg_lamps
    status_lamps = not status_lamps
    msg_lamps = "on" if status_lamps else "off"
    sio.emit("uvc-status", {"status": msg_lamps, "success": status_lamps})
    print("Conmutando lamparas UVC a:", msg_lamps)

@sio.on("stop-all")
def on_stop_all(data):
    global stop_robot
    stop_robot = not stop_robot
    sio.emit("stop-all-now", {"status": "stop", "success": stop_robot})
    print("Paro de emergencia activado")


@sio.on("solicitar-datos")
def solicitar_datos(data):
    # Simular datos de bateria
    bateria = random.randint(20, 100)
    c02 = random.randint(300, 600)
    sio.emit("datos-bateria", {"battery": bateria, "success": True})
    sio.emit("datos-co2", {"co2": c02, "success": True})
    print("Enviando datos de batería:", bateria)
    print("Enviando datos de CO2:", c02)

# Conectarse al servidor
   
sio.connect("http://debthk.local:5000")
# Mantener el cliente corriendo
try:
    sio.wait()
finally:
    sio.disconnect()
