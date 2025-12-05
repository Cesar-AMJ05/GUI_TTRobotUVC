from flask_socketio import SocketIO, emit


def register_robot_events(socketio):

    # Evento para conocer el estadus de conexion con el red
    @socketio.on("disconnect")
    def handle_is_disconnect():
        print("Emisor desconectado")
        emit("is-online", {"status": "offline", "success":False }, broadcast=True)
    @socketio.on("is-online")
    def handle_is_online(data):
        print("Estado del emisor:", data)
        emit("is-online", data, broadcast=True)


    # Evento para iniciar el proceso
    @socketio.on("start-process")
    def handle_start():
        emit("start-process", {"msg": "Inicia el proceso"}, broadcast=True)
    @socketio.on("go-robot")
    def handle_flag_start(data):
        print("Re - Robot", data)
        emit("go-robot", data, broadcast=True)
        emit("nueva_notificacion", {"msg": "▶️ Inicia el proceso"}, broadcast=True)


    # Evento para regreso a casa
    @socketio.on("move-home")
    def handle_home_btt():
        print("🔘 Botón Homet presionado")
        # Aquí puedes agregar la  lógica para manejar el botón Home
        emit("go-home", {"message": "Botón Home presionado"}, broadcast=True)
    @socketio.on("go-home")
    def handle_home_flag(data):
        print("RE - Regreso a cada", data)
        emit("nueva_notificacion", {"msg": "A casa 😛"}, broadcast=True)


    # Eventos para conmutar el estado de las lamparas UVC (para permitir que se enciendan)
    @socketio.on("toggle-LampsUVC")
    def handle_toggle_LUVC():
        emit("toggle-LampsUVC", {"msg": "Lamparas UVC activas"}, broadcast=True)
    @socketio.on("uvc-status")
    def handle_flag_UVC(data):
        print("Re - Toggle UVC: ", data)    
        emit("uvc-status", data, broadcast=True)
        if data.get("status")== "on":
            msg = "✅ Lamparas UVC activas"
        elif data.get("status") == "off":
            msg = "❌ Lamparas UVC desactivadas"
        else:
            msg = "❓ Estatus de lamparas desconocido"
        emit("nueva_notificacion", {"msg": msg}, broadcast=True)



    # Eventos para detener todo el robot
    @socketio.on("stop-all")
    def handle_emercy_stop():
        emit("stop-all", {"msg": "⚠️ Detener todos los procesos"}, broadcast= True)

    @socketio.on("stop-all-now")
    def handle_flag_stop(data):
        print("⚠️ Paro de emergencia")
        emit("stop-all-now", data, broadcast= True)
        emit("nueva_notificacion", {"msg": "⚠️ Paro de emergencia activado"}, broadcast=True)

