

# README – Transmisión de Cámara con FFmpeg y Flask

## 📌 Objetivo

Este proyecto permite transmitir el video de una cámara desde **Emisor o Dispositivo cliente** (en este caso Orange Pi 5 Max) a **servidor**, que actúa como servidor Flask, para mostrar el video en una página web.
El objetivo es mantener la **Emisor libre de carga**, evitando el uso directo de OpenCV para enviar frames.

---

## 📌 Por qué usar FFmpeg

**FFmpeg** es un conjunto de herramientas de código abierto para capturar, codificar y transmitir audio/video.
Ventajas sobre usar solo OpenCV o WebSockets:

| Característica            | FFmpeg                                   | OpenCV directo              | WebSockets (raw)                  |
| ------------------------- | ---------------------------------------- | --------------------------- | --------------------------------- |
| **Consumo CPU**           | Muy bajo (C optimizado)                  | Alto (Python codifica JPEG) | Medio-alto (codificación + envío) |
| **Latencia**              | Muy baja con `ultrafast` y `zerolatency` | Depende de Python           | Medio-alto                        |
| **Protocolos soportados** | UDP, TCP, RTSP, HTTP, HLS                | Solo video local            | TCP/WebSockets                    |
| **Escalabilidad**         | Alta (múltiples IPs)                     | Limitada                    | Limitada                          |
| **Hardware embebido**     | Optimizable (H.264 HW)                   | Muy pesado                  | Medio                             |

---

## 📌 Instalación de FFmpeg (Linux Debian 13)

Verificar si está instalado:

```bash
ffmpeg -version
```

Si no lo está:

```bash
sudo apt update
sudo apt install ffmpeg
```

---

## 📌 Verificar cámaras disponibles

```bash
v4l2-ctl --list-devices
```

Ejemplo de salida:

```
USB 2.0 Camera: USB 2.0 Camera (usb-0000:00:14.0-3):
    /dev/video2
    /dev/video3
Integrated Camera: Integrated C (usb-0000:00:14.0-6):
    /dev/video0
    /dev/video1
```

* Para cámara USB: usar `/dev/video2`.
* Para cámara integrada: usar `/dev/video0`.

---

## 📌 Prueba local en servidor

```bash
ffmpeg -f v4l2 -i /dev/video2 -vcodec mpeg1video -f mpegts udp://127.0.0.1:1235
```

* Python recibe el stream:

```python
import cv2

cap = cv2.VideoCapture("udp://127.0.0.1:1234")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se recibe frame")
        break
    cv2.imshow("Stream UDP", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
```

✅ Ventaja: ligero, confiable para pruebas locales.

---

## 📌 Producción (Orange Pi 5 Max)

```bash
ffmpeg -f v4l2 -i /dev/video2 -vcodec libx264 -preset ultrafast -tune zerolatency -f rtsp rtsp://127.0.0.1:8554/live.sdp
```

* Python / Flask recibe:

```python
cap = cv2.VideoCapture("rtsp://127.0.0.1:8554/live.sdp")
```

💡 Nota: RTSP requiere un **servidor RTSP** si quieres que otros dispositivos en la red accedan al stream.

---

## 📌 Flujo de transmisión

```
Emisor / Orange Pi 5 Max
    FFmpeg captura y codifica video
          │
          │ UDP / TCP / RTSP
          ▼
servidor (Servidor Flask)
    OpenCV recibe stream
    Flask sirve MJPEG
          │
          ▼
Página Web (<img src="/video_feed">)
    Video en tiempo real
```

* FFmpeg hace la codificación fuera de Python → CPU libre para otros procesos.
* OpenCV solo recibe y genera JPEG para web.
* MJPEG en Flask evita decodificar H.264 en el navegador.


