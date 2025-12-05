# backend/app/repositories/alert_repository.py
from datetime import datetime, date
from app.extensions import db
from app.models import Alert

class AlertRepository:
    
    # --- CAMBIO IMPORTANTE: Adaptado para recibir argumentos sueltos ---
    def create(self, **kwargs):
        """Crea una nueva alerta"""
        # Si no se proporciona fecha/hora, usar actual
        if 'fecha' not in kwargs:
            kwargs['fecha'] = date.today()
        if 'hora' not in kwargs:
            kwargs['hora'] = datetime.now().time()
        
        # Creamos la instancia con los datos desempaquetados
        alert = Alert(**kwargs)
        db.session.add(alert)
        db.session.commit()
        return alert
    
    def find_by_id(self, alert_id):
        """Busca alerta por ID"""
        return Alert.query.get(alert_id)
    
    def find_by_node(self, node_id, start_date=None, end_date=None):
        """Obtiene alertas de un nodo"""
        query = Alert.query.filter_by(nodo_id=node_id)
        
        if start_date:
            query = query.filter(Alert.fecha >= start_date)
        if end_date:
            query = query.filter(Alert.fecha <= end_date)
        
        return query.order_by(Alert.fecha.desc(), Alert.hora.desc()).all()
    
    def find_active(self):
        """Obtiene alertas activas"""
        return Alert.query.filter_by(estado='Activa')\
            .order_by(Alert.fecha.desc(), Alert.hora.desc()).all()
    
    def find_by_severity(self, severidad):
        """Obtiene alertas por severidad"""
        return Alert.query.filter_by(severidad=severidad, estado='Activa')\
            .order_by(Alert.fecha.desc(), Alert.hora.desc()).all()
    
    def update_status(self, alert_id, new_status):
        """Actualiza el estado de una alerta"""
        alert = Alert.query.get(alert_id)
        if alert:
            alert.estado = new_status
            db.session.commit()
        return alert
    
    def count_by_node(self, node_id, estado='Activa'):
        """Cuenta alertas de un nodo"""
        return Alert.query.filter_by(nodo_id=node_id, estado=estado).count()