# app.py 
# Servidor con Flask para la interfaz web del Modulo
# Se emplea Flask-SocketIO para la comunicación 

from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import cv2 
import time


#Ruta udp emisor de video por red local
ruta_udp_emisor = "udp://192.168.1.17:1236"

#Ruta udp local servidor  (para pruebas)
ruta_udp_local = "udp://127.0.0.1:1235"

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

camera_visible = True
error_imagen = cv2.imread("static/img/problemastecnicos.jpg")
if error_imagen is None:
    raise FileNotFoundError("No se pudo cargar la imagen de error. Verifica la ruta.")
#Ojo: Verificar el protocolo y la IP
"""
    Ojo: Verificar el protocolo y la IP
    Si se usa UDP O TCP
    Para produccio se recomienda  RTSP
"""

#cap = cv2.VideoCapture("udp://192.168.1.17:1236") 
#cap = cv2.imread("problemastecnicos.jpg")



def try2connectcamera(udp_emisor):
    """_summary_
        Intenta acceder a la camara por la ruta udp_emisor
    Args:
        udp_emisor (string): La ruta UDP de la cámara

    Raises:
        ValueError: Si no se puede acceder a la cámara

    Returns:
        _type_: Captura de video
    """
    
    cap = cv2.VideoCapture(udp_emisor) 
    if not cap.isOpened():
        cap.release()
        raise ValueError("No se puede acceder a la cámara")
    print("✅ Conectado a la cámara")
    return cap

def readFrame(cap):
    """
        Lee un frame de la captura de video
    Args:
        cap (object): Captura de video

    Raises:
        ValueError: Si no se puede leer el frame

    Returns:
        _type_: Frame de video
    """
    success, frame = cap.read()
    if not success:
        raise ValueError("No se puede leer el frame de la cámara")
    return frame

def codeframe(frame):
    """
        Codifica el frame en formato JPEG
    Args:
        frame (numpy.ndarray): Frame de video a codificar

    Raises:
        ValueError: Si no se puede codificar el frame

    Returns:
        bytes: Frame codificado en bytes
    """
    ret, buffer = cv2.imencode('.jpg', frame)
    if not ret:
        raise ValueError("No se puede codificar el frame")
    return buffer.tobytes()

def generate_frame(udp_emisor):
    """
        Genera frames para el stream de video, alternando entre la cámara y una imagen de error
    Args:
        udp_emisor (string): La ruta UDP de la cámara

    Yields:
        bytes: Frame de video codificado en bytes
    """
    global camera_visible, error_imagen
    cap = None

    while True:
        frame = error_imagen  # por defecto

        if camera_visible:
            try:
                # Conectar solo si no hay cap
                if cap is None:
                    cap = try2connectcamera(udp_emisor)
                # Si hay cámara, leer frame
                if cap is not None:
                    frame = readFrame(cap)

            except Exception as e:
                print(f"⚠️ Error con la cámara: {e}")
                if cap is not None:
                    cap.release()
                    cap = None
                frame = error_imagen
                time.sleep(2)  # espera antes de reintentar
        else:
            # 🔹 Toggle en OFF: solo mostrar imagen de error
            if cap is not None:
                cap.release()
                cap = None
            frame = error_imagen

        # Codificar y enviar el frame (ya sea cámara o imagen de error)
        try:
            frame_bytes = codeframe(frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        except Exception as e:
            print(f"⚠️ Error al procesar el frame: {e}")
            frame = error_imagen
            continue

#Ruta de la página principal
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/control.html")
def control():
    return render_template("control.html")

#Ruta para el stream de video
@app.route("/video_feed")
def video_feed():
    return Response(generate_frame(ruta_udp_local),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# Evento para alternar la visibilidad de la cámara
@socketio.on("toggle_camera")
def toggle_camera():
    global camera_visible
    camera_visible = not camera_visible
    print(f"📷 Estado cámara: {'visible' if camera_visible else 'oculta'}")
    # Avisar a todos los clientes conectados
    emit("camera_status", {"visible": camera_visible}, broadcast=True)

@socketio.on("go_home")
def handle_home_btt():
    print("🔘 Botón Homet presionado")
    # Aquí puedes agregar la lógica para manejar el botón Home
    emit("home_response", {"message": "Botón Home presionado"}, broadcast=True)


# Evitar debug=True mientras pruebas stream MJPEG
socketio.run(app, host='0.0.0.0', port=5000, debug=False)

