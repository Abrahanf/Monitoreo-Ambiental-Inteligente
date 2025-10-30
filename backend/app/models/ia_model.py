# backend/app/models/ia_model.py
from datetime import datetime
from app.extensions import db

class IAModel(db.Model):
    __tablename__ = 'modelos_ia'
    
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(50), nullable=False, unique=True)
    precision = db.Column(db.Float, nullable=False)
    sensibilidad = db.Column(db.Float, default=0.5)  # Threshold para detección
    dataset = db.Column(db.String(200), nullable=False)
    fecha_entrenamiento = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=False)
    parametros = db.Column(db.Text, nullable=True)  # JSON con hiperparámetros
    
    def to_dict(self):
        return {
            'id': self.id,
            'version': self.version,
            'precision': self.precision,
            'sensibilidad': self.sensibilidad,
            'dataset': self.dataset,
            'fecha_entrenamiento': self.fecha_entrenamiento.isoformat(),
            'activo': self.activo,
            'parametros': self.parametros
        }