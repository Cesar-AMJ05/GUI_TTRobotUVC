# routes/camera_routes.py

from flask import Response
from services.camara_service import generate_frame
from config import Config

def register_camera_routes(app):
    
    @app.route("/video_feed")
    def video_feed():
        return Response(
            generate_frame(Config.UDP_LOCAL),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )