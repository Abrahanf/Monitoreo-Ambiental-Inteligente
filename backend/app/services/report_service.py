# backend/app/services/report_service.py
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
import json
from app.repositories import ReportRepository, MeasurementRepository, AlertRepository, NodeRepository

class ReportService:
    @staticmethod
    def generate_report(user_id, node_ids, start_date, end_date):
        """Genera un reporte en PDF"""
        # Validar fechas
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
        
        # Crear documento PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Título
        title = Paragraph(
            f"<b>Reporte Ambiental</b><br/>{start_date.date()} - {end_date.date()}",
            styles['Title']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Por cada nodo
        for node_id in node_ids:
            node = NodeRepository.find_by_id(node_id)
            if not node:
                continue
            
            # Información del nodo
            node_info = Paragraph(f"<b>Nodo:</b> {node.ubicacion}", styles['Heading2'])
            elements.append(node_info)
            elements.append(Spacer(1, 0.2*inch))
            
            # Estadísticas
            stats = MeasurementRepository.get_statistics(node_id, start_date, end_date)
            
            data = [
                ['Variable', 'Promedio', 'Mínimo', 'Máximo'],
                ['Temperatura (°C)', 
                 f"{stats['temperatura']['promedio']:.2f}",
                 f"{stats['temperatura']['minimo']:.2f}",
                 f"{stats['temperatura']['maximo']:.2f}"],
                ['Humedad (%)', 
                 f"{stats['humedad']['promedio']:.2f}",
                 f"{stats['humedad']['minimo']:.2f}",
                 f"{stats['humedad']['maximo']:.2f}"],
                ['CO2 (ppm)', 
                 f"{stats['co2']['promedio']:.2f}",
                 f"{stats['co2']['minimo']:.2f}",
                 f"{stats['co2']['maximo']:.2f}"],
            ]
            
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Alertas
            alerts = AlertRepository.find_by_node(node_id, start_date.date(), end_date.date())
            if alerts:
                alert_title = Paragraph("<b>Alertas Generadas:</b>", styles['Heading3'])
                elements.append(alert_title)
                
                alert_data = [['Fecha', 'Tipo', 'Severidad', 'Estado']]
                for alert in alerts[:10]:  # Primeras 10 alertas
                    alert_data.append([
                        str(alert.fecha),
                        alert.tipo,
                        alert.severidad,
                        alert.estado
                    ])
                
                alert_table = Table(alert_data)
                alert_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
                ]))
                elements.append(alert_table)
            
            elements.append(Spacer(1, 0.5*inch))
        
        # Construir PDF
        doc.build(elements)
        pdf_content = buffer.getvalue()
        buffer.close()
        
        # TODO: Subir a S3 y obtener URL
        archivo_url = None
        
        # Guardar registro del reporte
        periodo = f"{start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}"
        report_data = {
            'usuario_id': user_id,
            'periodo': periodo,
            'fecha_inicio': start_date.date(),
            'fecha_fin': end_date.date(),
            'nodos_incluidos': json.dumps(node_ids),
            'archivo_url': archivo_url
        }
        
        report = ReportRepository.create(report_data)
        
        return {
            'report': report.to_dict(),
            'pdf_content': pdf_content,
            'message': 'Reporte generado exitosamente'
        }, 201
    
    @staticmethod
    def get_user_reports(user_id):
        """Obtiene los reportes de un usuario"""
        reports = ReportRepository.find_by_user(user_id)
        return {'reports': [r.to_dict() for r in reports]}, 200
    
    @staticmethod
    def get_all_reports():
        """Obtiene todos los reportes"""
        reports = ReportRepository.find_all()
        return {'reports': [r.to_dict() for r in reports]}, 200
