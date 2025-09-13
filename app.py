# app.py 
# Servidor con Flask para la interfaz web del Modulo
# Se emplea Flask-SocketIO para la comunicación 

from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import cv2 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

camera_visible = True
#Ojo: Verificar el protocolo y la IP
"""
    Ojo: Verificar el protocolo y la IP
    Si se usa UDP O TCP
    Para produccio se recomienda  RTSP
"""
cap = cv2.VideoCapture("udp://127.0.0.1:1235") 



def generate_frames():
    while True:
        if not camera_visible:
            #Enviamos un frame obscuro
            frame = 255*np.ones((480, 640, 3), dtype=np.uint8)
        else:
            success, frame = cap.read()
            if not success:
                
                continue
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def home():
    return render_template("index.html")




@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on("toggle_camera")
def toggle_camera():
    global camera_visible
    camera_visible = not camera_visible
    print(f"📷 Estado cámara: {'visible' if camera_visible else 'oculta'}")
    # Avisar a todos los clientes conectados
    emit("camera_status", {"visible": camera_visible}, broadcast=True)

# Evitar debug=True mientras pruebas stream MJPEG
socketio.run(app, host='0.0.0.0', port=5000)

