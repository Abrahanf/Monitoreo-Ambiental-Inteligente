# backend/app/services/alert_service.py
from datetime import datetime, date
from app.repositories.alert_repository import AlertRepository
from app.repositories.sensor_repository import SensorRepository

class AlertService:
    def __init__(self):
        self.alert_repo = AlertRepository()
        self.sensor_repo = SensorRepository()

    # Esta es la función que llama el Worker
    def check_thresholds(self, nodo_id, temp, hum, co2):
        """Verifica umbrales recibiendo datos crudos"""
        
        # 1. Obtenemos la configuración de los sensores de la BD
        sensores = self.sensor_repo.get_by_node(nodo_id)
        
        if not sensores:
            return []

        alerts_created = []

        for sensor in sensores:
            # Si el sensor está apagado, lo ignoramos
            if sensor.estado == 'OFF':
                continue

            # 2. Mapeamos el dato que llegó con la variable del sensor
            value = None
            tipo_alerta = None

            # Ajusta estos strings según lo que tengas en tu BD ('temperatura' o 'temp')
            if sensor.variable in ['temp', 'temperatura', 'Temperatura']:
                value = temp
                tipo_alerta = 'Temperatura'
            elif sensor.variable in ['hum', 'humedad', 'Humedad']:
                value = hum
                tipo_alerta = 'Humedad'
            elif sensor.variable in ['co2', 'CO2']:
                value = co2
                tipo_alerta = 'CO2'

            # Si no llegó dato para este sensor, pasamos
            if value is None:
                continue

            # 3. Lógica de verificación (Tu lógica original)
            umbral_superado = None
            mensaje = ""

            if sensor.umbral_min is not None and value < sensor.umbral_min:
                umbral_superado = sensor.umbral_min
                mensaje = f'{tipo_alerta} por debajo del mínimo ({value} < {umbral_superado})'
            
            elif sensor.umbral_max is not None and value > sensor.umbral_max:
                umbral_superado = sensor.umbral_max
                mensaje = f'{tipo_alerta} por encima del máximo ({value} > {umbral_superado})'

            # 4. Si hubo problema, creamos la alerta
            if umbral_superado:
                # Usamos tu cálculo de severidad
                severidad = self._calculate_severity(value, sensor)

                # Preparamos los datos para el repositorio
                # Usamos argumentos nombrados (kwargs) como configuramos el repo
                alert = self.alert_repo.create(
                    nodo_id=nodo_id,
                    fecha=date.today(),
                    hora=datetime.now().time(),
                    tipo=tipo_alerta,
                    valor=value,
                    umbral=umbral_superado,
                    severidad=severidad,
                    estado='Activa',
                    mensaje=mensaje # Asegúrate que tu modelo Alerta tenga este campo, si no, quítalo
                )
                alerts_created.append(alert)
                print(f"🚨 ALERTA CREADA: {mensaje}")

        return alerts_created

    def _calculate_severity(self, value, sensor):
        """Tu lógica original de cálculo porcentual"""
        if not sensor.umbral_max or not sensor.umbral_min:
            return 'Media' # Fallback si faltan umbrales

        rango = sensor.umbral_max - sensor.umbral_min
        if rango == 0: return 'Alta'

        diff_percent = 0
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
