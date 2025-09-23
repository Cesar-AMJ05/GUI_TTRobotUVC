document.addEventListener("DOMContentLoaded", () => {
    // Elementos del DOM

        // Elementos de control manual
    const controlBtn = document.getElementById("control-int");

        // Elementos de barra de notificaciones
    const noti_bttn = document.getElementById("noti-bttn");
    const close_noti = document.getElementById("close-sidebar");
    const clear_noti = document.getElementById("clear-btn");
    const sidebar = document.getElementById("sidebar");
    const no_noti_msg = document.getElementById("no-noti-msg");
    const badge_count = document.getElementById("badge");
    let notiCount = 0;
        // ELemetos de control de la camara
    const toggleBtn = document.getElementById("toggle-cam");
    const camIcon = document.getElementById("cam-icon");
    const camStream = document.getElementById("camera-stream");

        // Elementos de control 
    const startBtn = document.getElementById("start-btt");
    startBtn.disabled = false;

    const homeBtn = document.getElementById("home-btt");
    const UVCLampsBtn = document.getElementById("uvc-btt");

    const StopAllBtn = document.getElementById("stop-btt");
    StopAllBtn.disabled = true;

    // Elementos de monitoreo


    // Elemenmtos de visuales
        //Indicador de estado del conexion de robot
    const indicator_online = document.getElementById("indicator-online");
    const text_2ind_online = document.getAnimations("text-online");
        //Indicador de estado de lamparas UVC
    const indicator_lamps = document.getElementById("indicator-lamps");
    const text_2ind_lamps = document.getElementById("text-lamps");
        //Indicador del estado del robot
    const indicator_status = document.getElementById("indicator-status");
    const text_2ind_status = document.getElementById("text-status");


    // Variables 

    // Conexión SocketIO
    const socket = io();

    socket.on("connect", () =>{
        console.log("Navegador conectado al servidor");
        socket.emit("emisor-online");
    });

    // Escuchar estado de la cámara
    socket.on("camera_status", (data) => {
        if (data.visible === false) {
            camStream.src = "/static/img/no_video.png";
            camIcon.src = "/static/img/icon_no_video.png";
        } else {
            camStream.src = "/video_feed";
            camIcon.src = "/static/img/icon_video.png";
        }
    });

    //Boton "Start"
    startBtn.addEventListener("click", () => {
        socket.emit("start-process");
        startBtn.disabled = true;
        StopAllBtn.disabled = false;
    });

    // Botón "Home"
    homeBtn.addEventListener("click", () => {
        socket.emit("go_home");
    });

    // Evento para  "Lampras UVC"  
    UVCLampsBtn.addEventListener("click", () => {
        socket.emit("toggle-LampsUVC");
    });
    socket.on("uvc-status", (data) => {
        console.log("Estado de lamparas", data.status);
        if(data.success){
            indicator_lamps.classList.add("indicator-on");
            indicator_lamps.classList.remove("indicator-off");
            text_2ind_lamps.textContent = "Activado";
        } else {
            indicator_lamps.classList.add("indicator-off");
            indicator_lamps.classList.remove("indicator-on");
            text_2ind_lamps.textContent = "Desactivado";
        }
    });



    // Boton "Stop robot"
    StopAllBtn.addEventListener("click", () => {
        socket.emit("stop-all");

        startBtn.disabled = false;
        StopAllBtn.disabled = true;
    });

    socket.on("robot-is-connect", (data) =>{
        console.log("Estado del robot", (data));
        indicator_online.classList.add("indicator-on");
        indicator_online.classList.remove("indicator-off");
        text_2ind_online.textContent = "Conectado";
    });




    // Botón cámara
    toggleBtn.addEventListener("click", () => {
        socket.emit("toggle_camera");
    });

    // Redirigir a control manual
    controlBtn.addEventListener("click", () => {
        window.location.href = "/control.html";
    });

    // Abrir/cerrar sidebar
    noti_bttn.addEventListener("click", () =>{
        sidebar.classList.toggle("active");
        if(sidebar.classList.contains("active")){
            notiCount = 0;
            updateBadge();
        }
    });

    // Cerrar sidebar
    close_noti.addEventListener("click",() =>{
        sidebar.classList.remove("active");
    });

    // Nueva notificación
    socket.on("nueva_notificacion",(data)=>{
        let ul = document.querySelector("#noti-list ul");
        let li = document.createElement("li");
        li.textContent = data.msg;
        ul.appendChild(li);

        // Scroll automático
        let notiList = document.getElementById("noti-list");
        no_noti_msg.style.display = "none";
        notiList.scrollTop = notiList.scrollHeight;


        if(!sidebar.classList.contains("active")){
            notiCount++;
            updateBadge();
        }
    });

    // Limpiar notificaciones
    clear_noti.addEventListener("click", ()=>{
        socket.emit("limpiar");
    });

    socket.on("borrar", () => {
        let ul = document.querySelector("#noti-list ul");
        ul.innerHTML = "";
        no_noti_msg.style.display = "block";
    });

    function updateBadge(){
        if (notiCount>0){
            badge_count.style.display ="inline";
            badge_count.textContent = notiCount;
        }else{
            badge_count.style.display = "none";
        }
    }
    // Inicializa lista vacía
    let ul = document.querySelector("#noti-list ul");
    ul.innerHTML = "";
    no_noti_msg.style.display = "block";
});
