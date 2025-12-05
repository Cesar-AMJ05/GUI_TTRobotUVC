
# ========================================
# config.py - Configuración Central del Proyecto
# ========================================
"""
Este archivo centraliza TODAS las configuraciones que
actualmente tienes dispersas en tu app.py como variables globales.

VENTAJAS:
- Cambiar configuraciones sin tocar código
- Diferentes configs para desarrollo/producción
- Fácil de encontrar y modificar
- No repetir valores en múltiples archivos
"""

class Config:
    """Configuración general de la aplicación"""

    # CONFIGURACIÓN DE FLASK

    
    # Clave secreta para sesiones 
    SECRET_KEY = 'secret!'
    
    # Modo debug (False en producción)
    DEBUG = False
    
    # Host y puerto del servidor
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Orígenes permitidos para CORS
    CORS_ALLOWED_ORIGINS = "*"
    
    # Modo asíncrono
    ASYNC_MODE = 'threading'
    
    # RUTAS UDP PARA VIDEO
    
    # Ruta UDP del emisor de video (red local)
    UDP_EMISOR = "udp://192.168.0.200:1235"
    
    # Ruta UDP local para pruebas
    UDP_LOCAL = "udp://127.0.0.1:1235"
    
    # ========================================
    # CONFIGURACIÓN DE CÁMARA
    # Ruta de la imagen que se muestra cuando hay error
    ERROR_IMAGE_PATH = "static/img/problemastecnicos.jpg"
    
    # Estado inicial de la cámara (visible/oculta)
    CAMERA_VISIBLE = True
    
    # Tiempo de espera al reconectar (segundos)
    CAMERA_RECONNECT_DELAY = 2
    

  # CONFIGURACIÓN DEL ROBOT
  
    
    # Estados iniciales del robot
    ROBOT_START_PROCESS = True
    ROBOT_STOP_PROCESS = True
    ROBOT_TOGGLE_UVC_LAMP = False
    ROBOT_IS_CONNECTED = False
    
    # INTERVALOS DE TIEMPO
    
    # Intervalo para solicitar datos al emisor (segundos)
    DATA_REQUEST_INTERVAL = 15
    
    # ========================================
    # CONFIGURACIÓN DE LOGGING (OPCIONAL)
    # ========================================
    
    # Nivel de logging: DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_LEVEL = 'INFO'
    
    # Archivo de logs (None = solo consola)
    LOG_FILE = None  # 'logs/robot.log'


# ========================================
# CONFIGURACIÓN PARA DESARROLLO
# ========================================
class DevelopmentConfig(Config):
    """
    Configuración para ambiente de desarrollo
    Hereda de Config y sobrescribe algunos valores
    """
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    
    # Usar UDP local para pruebas sin robot
    UDP_EMISOR = Config.UDP_LOCAL

# ========================================
# CONFIGURACIÓN PARA PRODUCCIÓN
# ========================================
class ProductionConfig(Config):
    """
    Configuración para ambiente de producción
    """
    DEBUG = False
    
    # Usar clave secreta más segura (generada aleatoriamente)
    SECRET_KEY = 'tu_clave_secreta_super_segura_aqui_123456'
    
    # Usar UDP real del robot
    UDP_EMISOR = "udp://192.168.1.105:1236"
    
    # Activar logs en archivo
    LOG_FILE = 'logs/robot.log'


class TestingConfig(Config):
    """
    Configuración para pruebas unitarias
    """
    TESTING = True
    DEBUG = True
    
    # No usar video real en tests
    UDP_EMISOR = None
    CAMERA_VISIBLE = False


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': Config
}


def get_config(config_name='default'):
    """
    Obtiene la configuración según el nombre
    
    Args:
        config_name (str): Nombre de la configuración
                          ('development', 'production', 'testing', 'default')
    
    Returns:
        Config: Clase de configuración
    
    Ejemplo:
        >>> config = get_config('development')
        >>> print(config.DEBUG)
        True
    """
    return config_by_name.get(config_name, Config)