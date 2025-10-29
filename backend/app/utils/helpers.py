# backend/app/utils/helpers.py
from datetime import datetime, timedelta
import json

def parse_date_range(period):
    """Convierte un período en rango de fechas"""
    end_date = datetime.utcnow()
    
    if period == 'day':
        start_date = end_date - timedelta(days=1)
    elif period == 'week':
        start_date = end_date - timedelta(weeks=1)
    elif period == 'month':
        start_date = end_date - timedelta(days=30)
    else:
        start_date = end_date - timedelta(days=1)
    
    return start_date, end_date

def format_measurement_for_chart(measurements):
    """Formatea mediciones para gráficos"""
    return [{
        'timestamp': m.fecha_hora.isoformat(),
        'temperatura': m.temperatura,
        'humedad': m.humedad,
        'co2': m.co2
    } for m in measurements]

def calculate_alert_statistics(alerts):
    """Calcula estadísticas de alertas"""
    if not alerts:
        return {
            'total': 0,
            'por_severidad': {},
            'por_tipo': {}
        }
    
    stats = {
        'total': len(alerts),
        'por_severidad': {},
        'por_tipo': {}
    }
    
    for alert in alerts:
        # Por severidad
        if alert.severidad not in stats['por_severidad']:
            stats['por_severidad'][alert.severidad] = 0
        stats['por_severidad'][alert.severidad] += 1
        
        # Por tipo
        if alert.tipo not in stats['por_tipo']:
            stats['por_tipo'][alert.tipo] = 0
        stats['por_tipo'][alert.tipo] += 1
    
    return stats
