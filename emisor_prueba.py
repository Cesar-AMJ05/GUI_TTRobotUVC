import socketio

# Crear cliente SocketIO
sio = socketio.Client()

# Conectarse al servidor (IP de tu servidor Flask)
sio.connect("http://127.0.0.1:5000/")  # <- cambia la IP

# Escuchar el evento enviado desde la web
@sio.on("home-btt")
def on_home(data):
    print("🔘 Comando HOME recibido en el emisor")
    # Aquí agregas la lógica para mover el robot o lo que necesites
    # Por ejemplo:
    # mover_robot_a_home()

# También puedes escuchar responses del servidor
@sio.on("home_response")
def on_response(data):
    print("Mensaje del servidor:", data["message"])

# Mantener el cliente corriendo
sio.wait()
