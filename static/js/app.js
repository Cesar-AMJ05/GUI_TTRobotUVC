document.addEventListener("DOMContentLoaded", () => {
    // Elementos del DOM
    const toggleBtn = document.getElementById("toggle-cam");
    const camIcon = document.getElementById("cam-icon");
    const camStream = document.getElementById("camera-stream");

    // Conexión SocketIO
    const socket = io();

    // Escuchar el estado de la cámara desde el servidor
    socket.on("camera_status", (data) => {
        if (data.visible === false) {
            camStream.src = "/static/img/no_video.png"; // placeholder
            camIcon.src = "/static/img/icon_no_video.png";
        } else {
            camStream.src = "/video_feed"; // vuelve a mostrar el stream
            camIcon.src = "/static/img/icon_video.png";
        }
    });


    // Emitir evento al servidor al hacer click en el botón
    toggleBtn.addEventListener("click", () => {
        socket.emit("toggle_camera");
    });
});
