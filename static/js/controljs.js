document.addEventListener("DOMContentLoaded", () =>{

    const panel_bttn  = document.getElementById("panel-bttn");





    const socket = io();

    panel_bttn.addEventListener("click", () =>{
        window.location.href = "/"

    });

});