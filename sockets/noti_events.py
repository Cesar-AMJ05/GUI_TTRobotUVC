
from flask_socketio import SocketIO, emit

def noti_events(socketio):
        # Evento para alternar la visibilidad de la cámara
    @socketio.on("toggle_camera")
    def toggle_camera():
        global camera_visible
        camera_visible = not camera_visible
        print(f"📷 Estado cámara: {'visible' if camera_visible else 'oculta'}")
        # Avisar a todos los clientes conectados
        emit("camera_status", {"visible": camera_visible}, broadcast=True)



    #Eventos barra de notificaciones
    @socketio.on("limpiar")
    def handle_home():
        print("Notificaciones eliminadas")
        emit("borrar", broadcast=True)