# backend/app/blueprints/alerts.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.alert_service import AlertService

alerts_bp = Blueprint('alerts', __name__)
alert_service = AlertService() # <--- INSTANCIAMOS

@alerts_bp.route('', methods=['GET'])
@jwt_required()
def get_alerts():
    """Obtiene alertas activas"""
    # En tu AlertService no definimos 'get_active_alerts', 
    # pero podemos usar el repositorio directamente a través del servicio si quieres,
    # o mejor aún, implementa este método rápido en AlertService:
    
    # OPCIÓN RÁPIDA: Usar el repositorio del servicio
    alerts = alert_service.alert_repo.find_active()
    return jsonify([a.to_dict() for a in alerts]), 200
