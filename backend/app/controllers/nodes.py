# backend/app/blueprints/nodes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
# 1. Importar la clase correctamente
from app.services.node_service import NodeService 
from app.utils.decorators import validate_json, admin_required

nodes_bp = Blueprint('nodes', __name__)

# 2. INSTANCIAR EL SERVICIO (¡Esto es lo vital!)
node_service = NodeService()

@nodes_bp.route('', methods=['GET'])
@jwt_required()
def get_nodes():
    """Obtiene todos los nodos"""
    # 3. Usar la instancia (node_service) en vez de la clase
    result, status = node_service.get_all_nodes()
    return jsonify(result), status

@nodes_bp.route('/<int:node_id>', methods=['GET'])
@jwt_required()
def get_node(node_id):
    """Obtiene un nodo específico"""
    result, status = node_service.get_node(node_id)
    return jsonify(result), status

@nodes_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
@validate_json(['ubicacion'])
def create_node():
    """CU6: Crear nodo"""
    data = request.get_json()
    result, status = node_service.create_node(data)
    return jsonify(result), status

@nodes_bp.route('/<int:node_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_node(node_id):
    """CU6: Editar nodo"""
    data = request.get_json()
    result, status = node_service.update_node(node_id, data)
    return jsonify(result), status

@nodes_bp.route('/<int:node_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_node(node_id):
    """CU6: Eliminar nodo"""
    result, status = node_service.delete_node(node_id)
    return jsonify(result), status

@nodes_bp.route('/<int:node_id>/sensors', methods=['POST'])
@jwt_required()
@admin_required
@validate_json(['sensor', 'variable', 'umbral_min', 'umbral_max'])
def add_sensor(node_id):
    """CU6: Agregar sensor a nodo"""
    data = request.get_json()
    result, status = node_service.add_sensor(node_id, data)
    return jsonify(result), status

@nodes_bp.route('/sensors/<int:sensor_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_sensor(sensor_id):
    """CU6: Editar sensor"""
    data = request.get_json()
    result, status = node_service.update_sensor(sensor_id, data)
    return jsonify(result), status

@nodes_bp.route('/sensors/<int:sensor_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_sensor(sensor_id):
    """CU6: Eliminar sensor"""
    result, status = node_service.delete_sensor(sensor_id)
    return jsonify(result), status