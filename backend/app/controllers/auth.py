from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
# Asumo que tienes este decorador, si no, quítalo por ahora
from app.utils.decorators import validate_json 

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()  # <--- INSTANCIAMOS EL SERVICIO

@auth_bp.route('/login', methods=['POST'])
# @validate_json(['correo', 'contrasena']) # Usa 'contrasena' sin ñ
def login():
    """CU1: Inicio de sesión"""
    data = request.get_json()
    # Usamos la instancia 'auth_service', no la clase 'AuthService'
    password = data.get('contrasena') or data.get('contraseña')
    if not password:
        return jsonify({'error': 'Falta el campo contraseña'}), 400
        
    # Usamos la variable 'password' que ya capturamos
    result, status = auth_service.login(data['correo'], password)
    return jsonify(result), status

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    result, status = auth_service.request_password_reset(data['correo'])
    return jsonify(result), status

@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity() # Esto devuelve el ID como string
    data = request.get_json()
    result, status = auth_service.change_password(
        user_id,
        data['contrasena_actual'],
        data['contrasena_nueva']
    )
    return jsonify(result), status

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    # Usamos el repo que ya vive dentro del servicio
    user = auth_service.user_repo.find_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    return jsonify({'user': user.to_dict()}), 200