# backend/app/models/measurement.py
from datetime import datetime
from app.extensions import db

class Measurement(db.Model):
    __tablename__ = 'mediciones'
    
    id = db.Column(db.Integer, primary_key=True)
    nodo_id = db.Column(db.Integer, db.ForeignKey('nodos.id'), nullable=False, index=True)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    temperatura = db.Column(db.Float, nullable=False)
    humedad = db.Column(db.Float, nullable=False)
    co2 = db.Column(db.Float, nullable=False)
    
    # Índice compuesto para consultas frecuentes
    __table_args__ = (
        db.Index('idx_nodo_fecha', 'nodo_id', 'fecha_hora'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'nodo_id': self.nodo_id,
            'fecha_hora': self.fecha_hora.isoformat(),
            'temperatura': self.temperatura,
            'humedad': self.humedad,
            'co2': self.co2
        }

