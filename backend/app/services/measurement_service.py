# backend/app/services/measurement_service.py
from datetime import datetime, timedelta
from app.repositories import MeasurementRepository, NodeRepository, AlertRepository
from app.services.alert_service import AlertService
import requests

class MeasurementService:
    @staticmethod
    def save_measurement(data):
        """Guarda una nueva medición y verifica alertas"""
        node_id = data['nodo_id']
        
        # Validar que el nodo exista
        node = NodeRepository.find_by_id(node_id)
        if not node:
            return {'error': 'Nodo no encontrado'}, 404
        
        # Actualizar última conexión
        NodeRepository.update_last_connection(node_id)
        
        # Guardar medición
        measurement = MeasurementRepository.create(data)
        
        # Verificar umbrales y generar alertas
        AlertService.check_and_create_alerts(measurement, node)
        
        # Enviar a IA para análisis (asíncrono)
        try:
            # TODO: Implementar llamada asíncrona con Celery
            pass
        except Exception as e:
            print(f"Error al enviar a IA: {e}")
        
        return {'measurement': measurement.to_dict(), 'message': 'Medición guardada'}, 201
    
    @staticmethod
    def get_historical(node_id, period='day'):
        """Obtiene datos históricos"""
        node = NodeRepository.find_by_id(node_id)
        if not node:
            return {'error': 'Nodo no encontrado'}, 404
        
        # Calcular rango de fechas
        end_date = datetime.utcnow()
        if period == 'day':
            start_date = end_date - timedelta(days=1)
        elif period == 'week':
            start_date = end_date - timedelta(weeks=1)
        elif period == 'month':
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=1)
        
        # Obtener mediciones
        measurements = MeasurementRepository.find_by_node(node_id, start_date, end_date)
        
        # Obtener estadísticas
        stats = MeasurementRepository.get_statistics(node_id, start_date, end_date)
        
        return {
            'measurements': [m.to_dict() for m in measurements],
            'statistics': stats,
            'period': period
        }, 200
    
    @staticmethod
    def get_dashboard_data(node_id):
        """Obtiene datos para el dashboard"""
        node = NodeRepository.find_by_id(node_id)
        if not node:
            return {'error': 'Nodo no encontrado'}, 404
        
        # Última medición
        latest = MeasurementRepository.find_latest_by_node(node_id, 1)
        
        # Promedios últimas 24 horas
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=24)
        hourly_data = MeasurementRepository.get_hourly_averages(node_id, start_date, end_date)
        
        # Alertas activas
        alerts = AlertRepository.find_by_node(node_id)
        active_alerts = [a for a in alerts if a.estado == 'Activa']
        
        return {
            'node': node.to_dict(),
            'latest_measurement': latest[0].to_dict() if latest else None,
            'hourly_data': hourly_data,
            'active_alerts': [a.to_dict() for a in active_alerts]
        }, 200