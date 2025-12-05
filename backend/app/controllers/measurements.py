# backend/app/blueprints/measurements.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
# Importamos el servicio que SÍ implementamos
from app.services.monitoring_service import MonitoringService 

measurements_bp = Blueprint('measurements', __name__)
monitoring_service = MonitoringService() # <--- INSTANCIAMOS

@measurements_bp.route('/historical/<int:node_id>', methods=['GET'])
@jwt_required()
def get_historical(node_id):
    """CU4: Ver detalles históricos"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Llamamos al método que creamos en MonitoringService
    data = monitoring_service.get_historical_data(node_id, start_date, end_date)
    
    # Convertimos la lista de objetos a JSON
    return jsonify([m.to_dict() for m in data]), 200
