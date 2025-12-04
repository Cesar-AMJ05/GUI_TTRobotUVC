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

Dentro de los cuales mediante web sokets se  emiten las instrucciones correspondientes dependiendo de el evento a manejar

## 📌 Manejo de eventos

### ✅ Evento - Robot en línea  📶
#### Evento de conexión exitosa
Maneja el estado de conexión del robot con el servidor

| Paso | Dispositivo de salida | Evento/Comando | Receptor       | Datos                              | Efecto                      |
| ---- | --------------------- | -------------- | -------------- | ---------------------------------- | --------------------------- |
| 1    | Emisor Python         | connect        | Servidor Flask | {"status":"online","success":True} | Envia el estado de conexion |
| 2    | Servidor Flask        | is-online      | GUI            | {"status":"online","success":True} | Recibe el estado del emisor |
| 3    | GUI                   | is-online      | - - - - -      | {"status":"on","success": true}    | Actualiza UI en panel       |

### ✅ Evento - Inicio del Proceso ▶️
#### Boton  Inicio
Maneja el inicio del proceso de navegación (ojo este proces se puede sostener tambien por los nivelss de CO2)
| Paso | Dispositivo de salida | Evento/Comando | Receptor       | Datos                           | Efecto                      |
| ---- | --------------------- | -------------- | -------------- | ------------------------------- | --------------------------- |
| 1    | GUI                   | start-process  | Servidor Flask | Ninguno                         | Inicia el proceso           |
| 2    | Servidor Flask        | start-process  | Emisor Python  | {"msg":"..."}                   | Activa el handler en emisor |
| 3    | Emisor Python         | go-robot       | Servidor Flask | {"status":"on","success"\:true} | Inicia el regreso           |
| 4    | Servidor Flask        | go-robot       | GUI            | {"status":"on","success"\:true} | Actualiza UI en panel       |

### ✅ Evento - Regreso a casa 🏡
#### Boton  Casa
Maneja el regreso a casa del robot a un area deteminada como "Casa"
| Paso | Dispositivo de salida | Evento/Comando | Receptor       | Datos                           | Efecto                          |
| ---- | --------------------- | -------------- | -------------- | ------------------------------- | ------------------------------- |
| 1    | GUI                   | move-home   

   | Servidor Flask | Ninguno                         | Inicia el evento regreso a casa |
| 2    | Servidor Flask        | move-home      | Emisor Python  | {"msg":"..."}                   | Activa el handler en emisor     |
| 3    | Emisor Python         | go-home        | Servidor Flask | {"status":"on","success"\:true} | Inicia el regreso               |
| 4    | Servidor Flask        | go-home        | GUI            | {"status":"on","success"\:true} | Actualiza UI en panel           |

### ✅ Evento - Conmutar estado de lamparas UVC 💡
#### Boton Lamparas UVC
Maneja la conmutacion de las lamapras UVC, como control para permitir o no el proceso de desinfección

| Paso | Dispositivo de salida | Evento/Comando  | Receptor       | Datos                           | Efecto                      |
| ---- | --------------------- | --------------- | -------------- | ------------------------------- | --------------------------- |
| 1    | GUI                   | toggle-LampsUVC | Servidor Flask | Ninguno                         | Solicita cambio de lámpara  |
| 2    | Servidor Flask        | toggle-LampsUVC | Emisor Python  | {"msg":"..."}                   | Activa el handler en emisor |
| 3    | Emisor Python         | uvc-status      | Servidor Flask | {"status":"on","success"\:true} | Actualiza estado del emisor |
| 4    | Servidor Flask        | uvc-status      | GUI            | {"status":"on","success"\:true} | Actualiza UI en panel       |

### ✅ Evento - Paro de emergengia 🚩
#### Boton paro de emergencia 
Maneja el paro de emergencia del robot, deteniendo todos los procesos

| Paso | Dispositivo de salida | Evento/Comando | Receptor       | Datos                           | Efecto                                 |
| ---- | --------------------- | -------------- | -------------- | ------------------------------- | -------------------------------------- |
| 1    | GUI                   | stop-all       | Servidor Flask | Ninguno                         | Inicia el evento de paro de emergencia |
| 2    | Servidor Flask        | stop-all       | Emisor Python  | {"msg":"..."}                   | Activa el handler en emisor            |
| 3    | Emisor Python         | stop-all-now   | Servidor Flask | {"status":"on","success"\:true} | Actualiza estado del emisor            |
| 4    | Servidor Flask        | stop-all-now   | GUI            | {"status":"on","success"\:true} | Actualiza UI en panel                  |

## 📊 Captura de datos

### Nivel de bateria
El emisor envia de manera paralela el porcentaje de bateria
| Paso | Dispositivo de salida | Evento/Comando | Receptor       | Datos                           | Efecto                      |
| ---- | --------------------- | -------------- | -------------- | ------------------------------- | --------------------------- |
| 1    | Servidor Flask        | solicitar-datos| Emisor Python | {"request":"data"}              | Solicita datos al emisor  |
| 2    | Emisor Python         | datos-bateria  | Servidor Flask  | {"battery": num ,"success": true} | Envia datos de bateria     |
