document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("toggle-cam");
    const cameraPanel = document.getElementById("camera-panel");
    const camIcon = document.getElementById("cam-icon");
    const socket = io();  // ← solo aquí

    // Escuchar evento del servidor
    socket.on("camera_status", (data) => {
        console.log("Estado cámara recibido:", data);
        if (data.visible === false) {
            cameraPanel.style.display = "none";
            camIcon.src = "/static/img/icon_no_video.png";
        } else {
            cameraPanel.style.display = "block";
            camIcon.src = "/static/img/icon_video.png";
        }
    });

    // Emitir evento al servidor al hacer click
    toggleBtn.addEventListener("click", () => {
        socket.emit("toggle_camera");
    });
});
