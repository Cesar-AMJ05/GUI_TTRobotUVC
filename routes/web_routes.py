
# routes/web_routes.py
from flask import render_template

def register_web_routes(app):
    """Registra las rutas de páginas web"""    
    @app.route("/")
    def home():
        """Página principal - Panel de monitoreo"""
        return render_template("index.html")
    
    @app.route("/control.html")
    def control():
        """Página de control manual"""
        return render_template("control.html")