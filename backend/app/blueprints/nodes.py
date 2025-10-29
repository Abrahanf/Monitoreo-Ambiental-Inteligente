# backend/app/blueprints/nodes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services import NodeService
from app.utils.decorators import validate_json, admin_required

nodes_bp = Blueprint('nodes', __name__)

@nodes_bp.route('', methods=['GET'])
@jwt_required()
def get_nodes():
    """Obtiene todos los nodos"""
    result, status = NodeService.get_all_nodes()
    return jsonify(result), status

@nodes_bp.route('/<int:node_id>', methods=['GET'])
@jwt_required()
def get_node(node_id):
    """Obtiene un nodo específico"""
    result, status = NodeService.get_node(node_id)
    return jsonify(result), status

@nodes_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
@validate_json(['ubicacion'])
def create_node():
    """CU6: Crear nodo"""
    data = request.get_json()
    result, status = NodeService.create_node(data)
    return jsonify(result), status

@nodes_bp.route('/<int:node_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_node(node_id):
    """CU6: Editar nodo"""
    data = request.get_json()
    result, status = NodeService.update_node(node_id, data)
    return jsonify(result), status

@nodes_bp.route('/<int:node_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_node(node_id):
    """CU6: Eliminar nodo"""
    result, status = NodeService.delete_node(node_id)
    return jsonify(result), status

@nodes_bp.route('/<int:node_id>/sensors', methods=['POST'])
@jwt_required()
@admin_required
@validate_json(['sensor', 'variable', 'umbral_min', 'umbral_max'])
def add_sensor(node_id):
    """CU6: Agregar sensor a nodo"""
    data = request.get_json()
    result, status = NodeService.add_sensor(node_id, data)
    return jsonify(result), status

@nodes_bp.route('/sensors/<int:sensor_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_sensor(sensor_id):
    """CU6: Editar sensor"""
    data = request.get_json()
    result, status = NodeService.update_sensor(sensor_id, data)
    return jsonify(result), status

@nodes_bp.route('/sensors/<int:sensor_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_sensor(sensor_id):
    """CU6: Eliminar sensor"""
    result, status = NodeService.delete_sensor(sensor_id)
    return jsonify(result), status
