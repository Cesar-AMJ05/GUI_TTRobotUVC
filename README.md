# README - GUI del modulo de navegación autonoma para robot de desinfeccion con luz UVC 🤖

## 📌 Objetivo

Este proyecto permite controlar y monitorear el modulo de navegacion autonoma implementado en el robot omidireccional de desinfección con luz UVC.

De los procesos que nos permite monitorear son:

* Estado de la bateria
* Niveles de CO₂ en el ambiente
* Ubicacion en el mapa de el area de trabajo
* Vista de camara en live streaming
* Conexión con el servidor
* Estatus de las lámparas UVC
* Estatus de trabajo del robot

Por otro lado los proceso que controlamos

* Control de regreso a casa
* Control de activacion de lámparas UVC
* Control general "paro de emergencia"
* Control manual "teledirigido"

Para esto se emplea **FLask** en python para el desarrollo web, para el frontend se empelea **HTML+CSS**, y se emplea *JS* para vincular los eventos entre el servidor y el emisor. Para esto se emplea WebSokets. Estos sokets tiene las siguientes etiquetas

| Comando emitido | Tarea ejecutada                     |
| --------------- | ----------------------------------- |
| move-home       | Regreso a casa                      |
| toggle-LampUVC  | Encendido o apagado de lamparas UVC |
| stop-all        | Paro de emergencia                  |


Dentro de los cuales mediante web sokets se  emiten las instrucciones correspondientes dependiendo de el evento a manejar

## 📌 Manejo de eventos

### ✅ Evento - Regreso a casa 🏡
#### Boton  Casa




### ✅ Evento - Conmutar estado de lamparas UVC 💡
#### Boton Lamparas UVC
| Paso | Dispositivo de salida | Evento/Comando  | Receptor       | Datos                           | Efecto                      |
| ---- | --------------------- | --------------- | -------------- | ------------------------------- | --------------------------- |
| 1    | GUI                   | toggle-LampsUVC | Servidor Flask | Ninguno                         | Solicita cambio de lámpara  |
| 2    | Servidor Flask        | toggle-LampsUVC | Emisor Python  | {"msg":"..."}                   | Activa el handler en emisor |
| 3    | Emisor Python         | uvc-status      | Servidor Flask | {"status":"on","success"\:true} | Actualiza estado del emisor |
| 4    | Servidor Flask        | uvc-status      | GUI            | {"status":"on","success"\:true} | Actualiza UI en panel       |



