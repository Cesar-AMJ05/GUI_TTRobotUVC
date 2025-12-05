
from flask_socketio import SocketIO, emit
import random



# Eventos para actualizar datos del emisor

def register_data_emisor(socketio):

    # Datos de bateria
    @socketio.on("datos-bateria")
    def handle_datos_bateria(data):
        print("Datos de batería recibidos:", data)
        emit("datos-bateria", data, broadcast=True)
    #Datos de nivel de CO2
    @socketio.on("datos-co2")
    def handle_datos_co2(data):
        print("Datos de CO2 recibidos:", data)
        emit("datos-co2", data, broadcast=True)