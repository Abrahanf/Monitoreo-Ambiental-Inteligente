# backend/app/blueprints/reports.py
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import ReportService
from app.utils.decorators import validate_json
from io import BytesIO

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('', methods=['POST'])
@jwt_required()
@validate_json(['node_ids', 'fecha_inicio', 'fecha_fin'])
def generate_report():
    """CU5: Generar reportes"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    result, status = ReportService.generate_report(
        user_id,
        data['node_ids'],
        data['fecha_inicio'],
        data['fecha_fin']
    )
    
    if status == 201 and 'pdf_content' in result:
        # Retornar PDF directamente
        pdf_content = result.pop('pdf_content')
        return send_file(
            BytesIO(pdf_content),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'reporte_{result["report"]["id"]}.pdf'
        )
    
    return jsonify(result), status

@reports_bp.route('/my-reports', methods=['GET'])
@jwt_required()
def get_my_reports():
    """Obtiene reportes del usuario actual"""
    user_id = get_jwt_identity()
    result, status = ReportService.get_user_reports(user_id)
    return jsonify(result), status

@reports_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_reports():
    """Obtiene todos los reportes (solo admin)"""
    claims = get_jwt()
    if claims.get('rol') != 'administrador':
        return jsonify({'error': 'Acceso denegado'}), 403
    
    result, status = ReportService.get_all_reports()
    return jsonify(result), status