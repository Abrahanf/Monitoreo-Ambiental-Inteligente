# backend/app/models/report.py
from datetime import datetime
from app.extensions import db

class Report(db.Model):
    __tablename__ = 'reportes'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_generacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    periodo = db.Column(db.String(100), nullable=False)  # "Semana 42", "Enero 2025"
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    nodos_incluidos = db.Column(db.Text, nullable=False)  # JSON con IDs de nodos
    contenido = db.Column(db.Text, nullable=True)  # Resumen o análisis
    archivo_url = db.Column(db.String(500), nullable=True)  # URL en S3
    
    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'fecha_generacion': self.fecha_generacion.isoformat(),
            'periodo': self.periodo,
            'fecha_inicio': self.fecha_inicio.isoformat(),
            'fecha_fin': self.fecha_fin.isoformat(),
            'nodos_incluidos': self.nodos_incluidos,
            'contenido': self.contenido,
            'archivo_url': self.archivo_url
        }

