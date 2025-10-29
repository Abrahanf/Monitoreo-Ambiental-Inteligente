# backend/app/blueprints/measurements.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import MeasurementService

measurements_bp = Blueprint('measurements', __name__)

@measurements_bp.route('/dashboard/<int:node_id>', methods=['GET'])
@jwt_required()
def get_dashboard(node_id):
    """Obtiene datos para el dashboard"""
    result, status = MeasurementService.get_dashboard_data(node_id)
    return jsonify(result), status

@measurements_bp.route('/historical/<int:node_id>', methods=['GET'])
@jwt_required()
def get_historical(node_id):
    """CU4: Ver detalles históricos"""
    period = request.args.get('period', 'day')  # day, week, month
    result, status = MeasurementService.get_historical(node_id, period)
    return jsonify(result), status
