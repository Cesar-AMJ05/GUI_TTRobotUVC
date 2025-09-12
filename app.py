from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

camera_visible = True

@app.route("/")
def home():
    return render_template("index.html")



@socketio.on("toggle_camera")
def toggle_camera():
    global camera_visible
    camera_visible = not camera_visible
    print(f"📷 Estado cámara: {'visible' if camera_visible else 'oculta'}")
    # Avisar a todos los clientes conectados
    emit("camera_status", {"visible": camera_visible}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)

