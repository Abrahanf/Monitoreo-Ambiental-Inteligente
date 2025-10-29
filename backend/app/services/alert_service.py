# backend/app/services/alert_service.py
from datetime import datetime, date
from app.repositories import AlertRepository

class AlertService:
    @staticmethod
    def check_and_create_alerts(measurement, node):
        """Verifica umbrales y crea alertas si es necesario"""
        alerts_created = []
        
        # Obtener sensores del nodo
        for sensor in node.sensores:
            if sensor.estado == 'OFF':
                continue
            
            value = None
            tipo = None
            
            if sensor.variable == 'temp':
                value = measurement.temperatura
                tipo = 'Temperatura'
            elif sensor.variable == 'hum':
                value = measurement.humedad
                tipo = 'Humedad'
            elif sensor.variable == 'CO2':
                value = measurement.co2
                tipo = 'CO2'
            
            if value is None:
                continue
            
            # Verificar si se superó el umbral
            umbral_superado = None
            if value < sensor.umbral_min:
                umbral_superado = sensor.umbral_min
                mensaje = f'{tipo} por debajo del mínimo ({value} < {umbral_superado})'
            elif value > sensor.umbral_max:
                umbral_superado = sensor.umbral_max
                mensaje = f'{tipo} por encima del máximo ({value} > {umbral_superado})'
            
            if umbral_superado:
                # Determinar severidad
                severidad = AlertService._calculate_severity(value, sensor)
                
                # Crear alerta
                alert_data = {
                    'nodo_id': node.id,
                    'fecha': date.today(),
                    'hora': datetime.now().time(),
                    'tipo': tipo,
                    'valor': value,
                    'umbral': umbral_superado,
                    'severidad': severidad,
                    'estado': 'Activa',
                    'mensaje': mensaje
                }
                
                alert = AlertRepository.create(alert_data)
                alerts_created.append(alert)
        
        return alerts_created
    
    @staticmethod
    def _calculate_severity(value, sensor):
        """Calcula la severidad de una alerta"""
        # Calcular diferencia porcentual
        rango = sensor.umbral_max - sensor.umbral_min
        
        if value < sensor.umbral_min:
            diff_percent = abs((sensor.umbral_min - value) / rango) * 100
        else:
            diff_percent = abs((value - sensor.umbral_max) / rango) * 100
        
        if diff_percent > 50:
            return 'Crítica'
        elif diff_percent > 30:
            return 'Alta'
        elif diff_percent > 15:
            return 'Media'
        else:
            return 'Baja'
    
    @staticmethod
    def get_active_alerts(node_id=None):
        """Obtiene alertas activas"""
        if node_id:
            alerts = AlertRepository.find_by_node(node_id)
            alerts = [a for a in alerts if a.estado == 'Activa']
        else:
            alerts = AlertRepository.find_active()
        
        return {'alerts': [a.to_dict() for a in alerts]}, 200
    
    @staticmethod
    def update_alert_status(alert_id, new_status):
        """Actualiza el estado de una alerta"""
        alert = AlertRepository.update_status(alert_id, new_status)
        if not alert:
            return {'error': 'Alerta no encontrada'}, 404
        return {'alert': alert.to_dict(), 'message': 'Alerta actualizada'}, 200
