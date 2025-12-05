# backend/app/blueprints/users.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.services import UserService
from app.utils.decorators import validate_json, admin_required

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """Obtiene todos los usuarios"""
    result, status = UserService.get_all_users()
    return jsonify(result), status

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Obtiene un usuario específico"""
    result, status = UserService.get_user(user_id)
    return jsonify(result), status

@users_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
@validate_json(['nombre', 'correo'])
def create_user():
    """CU8: Crear usuario"""
    data = request.get_json()
    result, status = UserService.create_user(data)
    return jsonify(result), status

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    """CU9: Editar usuario"""
    data = request.get_json()
    result, status = UserService.update_user(user_id, data)
    return jsonify(result), status

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    """CU10: Eliminar usuario"""
    soft_delete = request.args.get('soft', 'true').lower() == 'true'
    result, status = UserService.delete_user(user_id, soft_delete)
    return jsonify(result), status

