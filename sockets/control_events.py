from flask_socketio import SocketIO, emit

def register_conotrol_events(socketio):
    
    @socketio.on('manual_control')
    def handle_manual_control(data):
        """
        Recibe comandos de control manual del joystick
        """
        
        direction = data.get('direction')
        action = data.get('action')
        timestamp = data.get('timestamp')
        
        print(f"📡 Control recibido: {action.upper()} - Dirección: {direction}")
        
        # ========================================
        # LÓGICA DE CONTROL DEL ROBOT
        # ========================================
        
        if action == 'press':
            print(f"▶️ Iniciando movimiento: {direction}")
            
            if direction == 'forward':
                print("🤖 Robot moviéndose hacia adelante")
            elif direction == 'backward':
                print("🤖 Robot moviéndose hacia atrás")
            elif direction == 'left':
                print("🤖 Robot girando a la izquierda")
            elif direction == 'right':
                print("🤖 Robot girando a la derecha")
            elif direction == 'forward_left':
                print("🤖 Robot moviéndose adelante-izquierda")
            elif direction == 'forward_right':
                print("🤖 Robot moviéndose adelante-derecha")
            elif direction == 'backward_left':
                print("🤖 Robot moviéndose atrás-izquierda")
            elif direction == 'backward_right':
                print("🤖 Robot moviéndose atrás-derecha")
            
            emit('control_response', {
                'status': 'success',
                'message': f'Movimiento iniciado: {direction}',
                'direction': direction,
                'action': action
            })
        
        elif action == 'release':
            print(f"⏹️ Deteniendo movimiento: {direction}")
            
            print("🤖 Robot detenido")
            
            emit('control_response', {
                'status': 'success',
                'message': 'Robot detenido',
                'direction': direction,
                'action': action
            })
        
        else:
            print(f"⚠️ Acción desconocida: {action}")
            emit('control_response', {
                'status': 'error',
                'message': f'Acción no reconocida: {action}'
            })

    # ========================================
    # MANEJADOR PARA EL BOTÓN DE BANDERA
    # ========================================
    @socketio.on('mark_waypoint')
    def handle_mark_waypoint(data):
        timestamp = data.get('timestamp')
        position = data.get('position', {})
        
        print(f"🚩 Marcando waypoint en timestamp: {timestamp}")
        
        emit('waypoint_response', {
            'status': 'success',
            'message': 'Punto de interés marcado',
            'waypoint_id': 1,
            'timestamp': timestamp
        })
