// ========================================
// CONTROL MANUAL DEL ROBOT - controljs.js
// ========================================

// Inicializar Socket.IO
const socket = io();

// Variable para rastrear el estado de los botones
let activeButton = null;
let isPressed = false;

// ========================================
// CONFIGURACIÓN DE BOTONES DE DIRECCIÓN
// ========================================

const directionButtons = {
    'up-btt': 'forward',
    'down-btt': 'backward',
    'left-btt': 'left',
    'right-btt': 'right',
    'up_left-btt': 'forward_left',
    'up_right-btt': 'forward_right',
    'down_left-btt': 'backward_left',
    'down_right-btt': 'backward_right'
};

// ========================================
// FUNCIÓN PARA ENVIAR COMANDO AL SERVIDOR
// ========================================

function sendMovementCommand(direction, action) {
    const command = {
        direction: direction,
        action: action, // 'press' o 'release'
        timestamp: Date.now()
    };
    
    console.log(`📡 Enviando comando:`, command);
    socket.emit('manual_control', command);
}

// ========================================
// FUNCIÓN PARA ACTIVAR FEEDBACK VISUAL
// ========================================

function activateButton(button) {
    button.classList.add('button-active');
    button.style.transform = 'scale(0.95)';
    button.style.boxShadow = '0 0 20px rgba(4, 255, 127, 0.8)';
}

function deactivateButton(button) {
    button.classList.remove('button-active');
    button.style.transform = 'scale(1)';
    button.style.boxShadow = 'none';
}

// ========================================
// MANEJADORES DE EVENTOS PARA CADA BOTÓN
// ========================================

Object.keys(directionButtons).forEach(buttonId => {
    const button = document.getElementById(buttonId);
    const direction = directionButtons[buttonId];
    
    if (!button) {
        console.warn(`⚠️ Botón ${buttonId} no encontrado`);
        return;
    }

    // ========================================
    // EVENTOS DE MOUSE (Desktop)
    // ========================================
    
    button.addEventListener('mousedown', (e) => {
        e.preventDefault(); // Evita selección de texto
        
        if (isPressed) return; // Ya hay un botón presionado
        
        isPressed = true;
        activeButton = button;
        
        activateButton(button);
        sendMovementCommand(direction, 'press');
    });

    button.addEventListener('mouseup', (e) => {
        e.preventDefault();
        
        if (activeButton === button) {
            isPressed = false;
            activeButton = null;
            
            deactivateButton(button);
            sendMovementCommand(direction, 'release');
        }
    });

    button.addEventListener('mouseleave', (e) => {
        // Si el mouse sale del botón mientras está presionado
        if (activeButton === button) {
            isPressed = false;
            activeButton = null;
            
            deactivateButton(button);
            sendMovementCommand(direction, 'release');
        }
    });

    // ========================================
    // EVENTOS TOUCH (Móviles/Tablets)
    // ========================================
    
    button.addEventListener('touchstart', (e) => {
        e.preventDefault(); // Evita zoom y scroll
        
        if (isPressed) return;
        
        isPressed = true;
        activeButton = button;
        
        activateButton(button);
        sendMovementCommand(direction, 'press');
    });

    button.addEventListener('touchend', (e) => {
        e.preventDefault();
        
        if (activeButton === button) {
            isPressed = false;
            activeButton = null;
            
            deactivateButton(button);
            sendMovementCommand(direction, 'release');
        }
    });

    button.addEventListener('touchcancel', (e) => {
        // Si el toque se cancela (sale del área, interrumpe, etc)
        if (activeButton === button) {
            isPressed = false;
            activeButton = null;
            
            deactivateButton(button);
            sendMovementCommand(direction, 'release');
        }
    });
});

// ========================================
// EVENTOS GLOBALES DE SEGURIDAD
// ========================================

// Si se suelta el mouse fuera de cualquier botón
document.addEventListener('mouseup', () => {
    if (isPressed && activeButton) {
        const direction = directionButtons[activeButton.id];
        
        isPressed = false;
        deactivateButton(activeButton);
        sendMovementCommand(direction, 'release');
        activeButton = null;
    }
});

// Si se levantan todos los dedos de la pantalla
document.addEventListener('touchend', () => {
    if (isPressed && activeButton) {
        const direction = directionButtons[activeButton.id];
        
        isPressed = false;
        deactivateButton(activeButton);
        sendMovementCommand(direction, 'release');
        activeButton = null;
    }
});

// ========================================
// BOTONES DE LA BARRA SUPERIOR
// ========================================

// Botón de regreso al panel de monitoreo
const panelButton = document.getElementById('panel-bttn');
if (panelButton) {
    panelButton.addEventListener('click', () => {
        // Asegurarse de detener cualquier movimiento antes de salir
        if (isPressed && activeButton) {
            const direction = directionButtons[activeButton.id];
            sendMovementCommand(direction, 'release');
        }
        
        console.log('🔙 Regresando al panel de monitoreo...');
        window.location.href = '/';
    });
}

// Botón de bandera (preparado para funcionalidad futura)
const flagButton = document.getElementById('flag-bttn');
if (flagButton) {
    flagButton.addEventListener('click', () => {
        console.log('🚩 Botón de bandera presionado (funcionalidad pendiente)');
        // TODO: Implementar funcionalidad de bandera
        // Posibles usos: marcar posición, establecer waypoint, etc.
    });
}

// Botón de notificaciones (preparado para funcionalidad futura)
const notificationButton = document.getElementById('notification-bttn');
if (notificationButton) {
    notificationButton.addEventListener('click', () => {
        console.log('🔔 Botón de notificaciones presionado (funcionalidad pendiente)');
        // TODO: Implementar panel de notificaciones
        // Similar al sidebar del panel principal
    });
}

// ========================================
// MANEJO DE DESCONEXIÓN
// ========================================

socket.on('connect', () => {
    console.log('✅ Conectado el control al servidor');
});

socket.on('disconnect', () => {
    console.log('❌ Desconectado el control del servidor');
    
    // Si se desconecta mientras hay un botón presionado
    if (isPressed && activeButton) {
        isPressed = false;
        deactivateButton(activeButton);
        activeButton = null;
    }
});

// ========================================
// RESPUESTA DEL SERVIDOR (Opcional)
// ========================================

socket.on('control_response', (data) => {
    console.log('📨 Respuesta del servidor:', data);
    
    // Aquí puedes manejar confirmaciones o errores del servidor
    if (data.status === 'error') {
        console.error('❌ Error en control:', data.message);
        // Podrías mostrar una notificación al usuario
    }
});

// ========================================
// PREVENCIÓN DE COMPORTAMIENTOS NO DESEADOS
// ========================================

// Evitar que se pueda arrastrar las imágenes
document.querySelectorAll('.joy-button img, .robotito').forEach(img => {
    img.addEventListener('dragstart', (e) => e.preventDefault());
});

// Evitar el menú contextual en los botones (click derecho)
document.querySelectorAll('.joy-button').forEach(button => {
    button.addEventListener('contextmenu', (e) => e.preventDefault());
});

console.log('🎮 Control manual inicializado correctamente');