# backend/app/repositories/report_repository.py
from app.extensions import db
from app.models import Report

class ReportRepository:
    @staticmethod
    def create(report_data):
        """Crea un nuevo reporte"""
        report = Report(**report_data)
        db.session.add(report)
        db.session.commit()
        return report
    
    @staticmethod
    def find_by_id(report_id):
        """Busca reporte por ID"""
        return Report.query.get(report_id)
    
    @staticmethod
    def find_by_user(user_id, limit=50):
        """Obtiene reportes de un usuario"""
        return Report.query.filter_by(usuario_id=user_id)\
            .order_by(Report.fecha_generacion.desc())\
            .limit(limit).all()
    
    @staticmethod
    def find_all(limit=100):
        """Obtiene todos los reportes"""
        return Report.query.order_by(Report.fecha_generacion.desc())\
            .limit(limit).all()
    
    @staticmethod
    def delete(report_id):
        """Elimina un reporte"""
        report = Report.query.get(report_id)
        if report:
            db.session.delete(report)
            db.session.commit()
        return report