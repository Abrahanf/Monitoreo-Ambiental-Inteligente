# backend/app/blueprints/alerts.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import AlertService
from app.utils.decorators import admin_required

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('', methods=['GET'])
@jwt_required()
def get_alerts():
    """Obtiene alertas activas"""
    node_id = request.args.get('node_id', type=int)
    result, status = AlertService.get_active_alerts(node_id)
    return jsonify(result), status

@alerts_bp.route('/<int:alert_id>/status', methods=['PUT'])
@jwt_required()
def update_alert_status(alert_id):
    """Actualiza el estado de una alerta"""
    data = request.get_json()
    new_status = data.get('estado', 'Resuelta')
    result, status = AlertService.update_alert_status(alert_id, new_status)
    return jsonify(result), status

