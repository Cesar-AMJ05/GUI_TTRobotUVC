import socketio

status_lamps = False;
msg_lamps = "off"


# Crear cliente SocketIO
sio = socketio.Client()

@sio.event
def connect():
    print("Emisor conectado al servidor")

@sio.event
def disconnect():
    print("Emisor desconectado al servidor")

# Escuchar el evento enviado desde la web
@sio.on("home-btt")
def on_home(data):
    print("🔘 Comando HOME recibido en el emisor")
    # Aquí agregas la lógica para mover el robot o lo que necesites
    # Por ejemplo:
    # mover_robot_a_home()


# Evento de conmutacion de lamparas UVC
@sio.on("toggle-LampsUVC")
def toggle_lamps(data):
    global status_lamps, msg_lamps

    status_lamps = not status_lamps  # más claro que XOR
    msg_lamps = "on" if status_lamps else "off"

    sio.emit("uvc-status", {
        "status": msg_lamps,
        "success": status_lamps
    })



# También puedes escuchar responses del servidor
@sio.on("home_response")
def on_response(data):
    print("Mensaje del servidor:", data["message"])


# Conectarse al servidor (IP de tu servidor Flask)
#sio.connect("http://192.168.1.17:5000/")  # <- cambia la IP
sio.connect("http://127.0.0.1:5000")

# Mantener el cliente corriendo
sio.wait()
