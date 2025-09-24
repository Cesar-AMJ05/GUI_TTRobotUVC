import socketio
import serial
import time
import atexit

status_start = False
stop_robot = False
status_lamps = False
msg_lamps = "off"

# Puerto COM
arduino = serial.Serial('COM6', 9600, timeout=1)  
time.sleep(2)  # Esperar a que Arduino se inicialice


# Registrar cierre seguro del serial
def cerrar_serial():
    if arduino.is_open:
        arduino.close()
        print("Puerto serial cerrado ")

atexit.register(cerrar_serial)

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
    arduino.write(b'A')
    arduino.flush()

@sio.on("go-home")
def go_home(data):
    sio.emit("go-home", {"status": "home", "success": True })
    arduino.write(b'C')
    arduino.flush()

@sio.on("toggle-LampsUVC")
def toggle_lamps(data):
    global status_lamps, msg_lamps
    status_lamps = not status_lamps
    msg_lamps = "on" if status_lamps else "off"
    sio.emit("uvc-status", {"status": msg_lamps, "success": status_lamps})
    arduino.write(b'B')
    arduino.flush()

@sio.on("stop-all")
def on_stop_all(data):
    global stop_robot
    stop_robot = not stop_robot
    sio.emit("stop-all-now", {"status": "stop", "success": stop_robot})
    arduino.write(b'A')
    arduino.flush()

# Conectarse al servidor
sio.connect("http://192.168.0.108:5000")

# Mantener el cliente corriendo
try:
    sio.wait()
finally:
    cerrar_serial()  # Cierra el puerto si se interrumpe con Ctrl+C
