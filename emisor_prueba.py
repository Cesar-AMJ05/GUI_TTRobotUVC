import socketio

status_start = False
stop_robot = False
status_lamps = False
msg_lamps = "off"

# Crear cliente SocketIO
sio = socketio.Client(reconnection=True, reconnection_attempts=5, reconnection_delay=2)

# Evento : Emisor conectado
@sio.event
def connect():
    print("✅ Conectado al servidor")
    # Aquí ya es seguro emitir cualquier evento
    sio.emit("is-online", {"status": "online", "success": True})

@sio.event
def disconnect():
    print("Me desconecte del servidor 😴")


# Evento : Regreso a casa 
@sio.on("home-btt")
def on_home(data):
    print("🔘 Comando HOME recibido en el emisor")
    # Aquí agregas la lógica para mover el robot o lo que necesites
    # Por ejemplo:
    # mover_robot_a_home()


# Evento : Iniciar proceso
@sio.on("start-process")
def start_robot(data):
    global start_robot
    print("Inicia el proceso del robot")
    start_robot = not start_robot
    sio.emit("go-robot", {
        "status": "go",
        "success":start_robot
        })

# También puedes escuchar responses del servidor
@sio.on("home_response")
def on_response(data):
    print("Mensaje del servidor:", data["message"])


# Evento : Conmutacion de lamparas UVC
@sio.on("toggle-LampsUVC")
def toggle_lamps(data):
    global status_lamps, msg_lamps

    status_lamps = not status_lamps  # más claro que XOR
    msg_lamps = "on" if status_lamps else "off"

    sio.emit("uvc-status", {
        "status": msg_lamps,
        "success": status_lamps
    })


#Evento : Paro de emergencia
@sio.on("stop-all")
def on_stop_all(data):
    global stop_robot
    stop_robot = not stop_robot
    sio.emit("stop-all-now",{
        "status": "stop",
        "success": stop_robot
        })

# Conectarse al servidor (IP de tu servidor Flask)
#sio.connect("http://192.168.1.17:5000/")  # <- cambia la IP
sio.connect("http://127.0.0.1:5000")

# Mantener el cliente corriendo
sio.wait()
