
# ========================================
# services/camera_service.py
# Servicio completo para manejo de cámara
# ========================================

import cv2
import time
from config import Config

# ========================================
# VARIABLES GLOBALES DEL SERVICIO
# ========================================

# Estado de visibilidad de la cámara
camera_visible = Config.CAMERA_VISIBLE

# Cargar imagen de error una sola vez
error_imagen = cv2.imread(Config.ERROR_IMAGE_PATH)

if error_imagen is None:
    raise FileNotFoundError(f"❌ No se pudo cargar: {Config.ERROR_IMAGE_PATH}")
else:
    print(f"✅ Imagen de error cargada: {Config.ERROR_IMAGE_PATH}")



def try2connectcamera(udp_emisor):
    """
    Intenta conectar a la cámara por UDP
    
    Esta función es la MISMA que tienes en tu app.py,
    solo que ahora está en un módulo separado.
    
    Args:
        udp_emisor (str): Ruta UDP de la cámara
                          Ejemplo: "udp://192.168.1.105:1236"
    
    Returns:
        cv2.VideoCapture: Objeto de captura de video
    
    Raises:
        ValueError: Si no se puede acceder a la cámara
    """
    cap = cv2.VideoCapture(udp_emisor)
    
    if not cap.isOpened():
        cap.release()
        raise ValueError(f"No se puede acceder a la cámara en {udp_emisor}")
    
    print(f"✅ Conectado a la cámara: {udp_emisor}")
    return cap


def readFrame(cap):
    """
    Lee un frame de la captura de video
    
    Esta es tu función readFrame, movida aquí.
    
    Args:
        cap (cv2.VideoCapture): Objeto de captura de video
    
    Returns:
        numpy.ndarray: Frame capturado
    
    Raises:
        ValueError: Si no se puede leer el frame
    """
    success, frame = cap.read()
    
    if not success:
        raise ValueError("No se puede leer el frame de la cámara")
    
    return frame


def codeframe(frame):
    """
    Codifica el frame en formato JPEG
    
    Esta es tu función codeframe, movida aquí.
    
    Args:
        frame (numpy.ndarray): Frame de video a codificar
    
    Returns:
        bytes: Frame codificado en bytes (JPEG)
    
    Raises:
        ValueError: Si no se puede codificar el frame
    """
    ret, buffer = cv2.imencode('.jpg', frame)
    
    if not ret:
        raise ValueError("No se puede codificar el frame")
    
    return buffer.tobytes()



def generate_frame(udp_emisor):
    """
    Generador de frames para streaming MJPEG
    
    Esta es tu función generate_frame, EXACTAMENTE igual,
    pero ahora usa las variables globales de este módulo.
    
    Args:
        udp_emisor (str): Ruta UDP de la cámara
    
    Yields:
        bytes: Frame codificado en formato multipart/x-mixed-replace
    """
    global camera_visible, error_imagen
    cap = None

    while True:
        frame = error_imagen  # Frame por defecto

        if camera_visible:
            try:
                # Intentar conectar si no hay conexión
                if cap is None:
                    cap = try2connectcamera(udp_emisor)
                
                # Leer frame si hay conexión
                if cap is not None:
                    frame = readFrame(cap)
                    frame = cv2.flip(frame, -1)  # Voltear 180°
                    
            except Exception as e:
                print(f"⚠️ Error con la cámara: {e}")
                
                # Liberar captura en caso de error
                if cap is not None:
                    cap.release()
                    cap = None
                
                frame = error_imagen
                time.sleep(2)  # Esperar antes de reintentar
        else:
            # Si la cámara está oculta, liberar captura
            if cap is not None:
                cap.release()
                cap = None
            frame = error_imagen

        # 🔹 Siempre devolver algo al navegador
        try:
            frame_bytes = codeframe(frame)
        except Exception as e:
            print(f"⚠️ Error al procesar el frame: {e}")
            frame_bytes = codeframe(error_imagen)

        # Formato MJPEG multipart
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def set_camera_visibility(visible):
    """
    Cambia el estado de visibilidad de la cámara
    
    NUEVA función para controlar la visibilidad desde
    otros módulos sin acceder directamente a la variable global.
    
    Args:
        visible (bool): True para mostrar, False para ocultar
    
    Returns:
        bool: Nuevo estado de visibilidad
    """
    global camera_visible
    camera_visible = visible
    status = "visible" if camera_visible else "oculta"
    print(f"📷 Estado cámara cambiado: {status}")
    return camera_visible


def get_camera_visibility():
    """
    Obtiene el estado actual de visibilidad de la cámara
    
    Returns:
        bool: True si visible, False si oculta
    """
    return camera_visible


def toggle_camera_visibility():
    """
    Alterna el estado de visibilidad de la cámara
    
    Returns:
        bool: Nuevo estado después de alternar
    """
    global camera_visible
    camera_visible = not camera_visible
    status = "visible" if camera_visible else "oculta"
    print(f"📷 Cámara alternada: ahora está {status}")
    return camera_visible


def init_camera_service():
    """
    Inicializa el servicio de cámara
    Verifica que todo esté listo antes de empezar
    """
    print("📸 Inicializando servicio de cámara...")
    print(f"   - Ruta UDP: {Config.UDP_EMISOR}")
    print(f"   - Imagen error: {Config.ERROR_IMAGE_PATH}")
    print(f"   - Estado inicial: {'visible' if camera_visible else 'oculta'}")
    print("✅ Servicio de cámara listo")


# Ejecutar al importar el módulo
init_camera_service()