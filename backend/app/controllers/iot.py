# backend/app/blueprints/iot.py
from flask import Blueprint, request, jsonify
from app.services import MeasurementService
from app.utils.decorators import validate_json

iot_bp = Blueprint('iot', __name__)

@iot_bp.route('/measurement', methods=['POST'])
@validate_json(['nodo_id', 'temperatura', 'humedad', 'co2'])
def receive_measurement():
    """Endpoint para recibir mediciones desde IoT (HTTP)"""
    data = request.get_json()
    result, status = MeasurementService.save_measurement(data)
    return jsonify(result), status