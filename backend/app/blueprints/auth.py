# backend/app/blueprints/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import AuthService
from app.utils.decorators import validate_json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@validate_json(['correo', 'contraseña'])
def login():
    """CU1: Inicio de sesión"""
    data = request.get_json()
    result, status = AuthService.login(data['correo'], data['contraseña'])
    return jsonify(result), status

@auth_bp.route('/forgot-password', methods=['POST'])
@validate_json(['correo'])
def forgot_password():
    """CU2: Olvidó contraseña"""
    data = request.get_json()
    result, status = AuthService.request_password_reset(data['correo'])
    return jsonify(result), status

@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
@validate_json(['contraseña_actual', 'contraseña_nueva'])
def change_password():
    """CU3: Cambiar contraseña"""
    user_id = get_jwt_identity()
    data = request.get_json()
    result, status = AuthService.change_password(
        user_id,
        data['contraseña_actual'],
        data['contraseña_nueva']
    )
    return jsonify(result), status

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Obtiene información del usuario actual"""
    from app.repositories import UserRepository
    user_id = get_jwt_identity()
    user = UserRepository.find_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

