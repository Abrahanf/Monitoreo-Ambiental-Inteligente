from app.repositories.measurement_repository import MeasurementRepository
from app.repositories.node_repository import NodeRepository
from app.services.alert_service import AlertService
from datetime import datetime

class MonitoringService:
    def __init__(self):
        # Inicializamos los repositorios para acceder a la BD
        self.measurement_repo = MeasurementRepository()
        self.node_repo = NodeRepository()
        # Inicializamos el servicio de alertas para verificar umbrales
        self.alert_service = AlertService()

    def register_measurement(self, nodo_id, temp, hum, co2):
        """
        Recibe datos crudos del MQTT, valida el nodo, guarda y verifica alertas.
        """
        # 1. Buscar el nodo por su MAC (física)
        nodo = self.node_repo.find_by_id(nodo_id)
        
        if not nodo:
            print(f"⚠️ ADVERTENCIA: Se recibió dato de nodo_id {nodo_id} pero no está registrado en BD.")
            # Opcional: Podrías auto-crear el nodo aquí si quisieras 'Plug & Play'
            return None

        # 2. Guardar la medición en la base de datos
        medicion = self.measurement_repo.create(
            nodo_id=nodo.id,
            temperatura=temp,
            humedad=hum,
            co2=co2,
            fecha_hora=datetime.utcnow()
        )

        # 3. Verificar si estos valores disparan alguna alerta
        # (Esto implementa el RF-5.2 del documento)
        self.alert_service.check_thresholds(nodo.id, temp, hum, co2)

        return medicion

    def get_historical_data(self, nodo_id, start_date=None, end_date=None):
        """
        Para el Dashboard (CU4): Recupera historial filtrado por fecha.
        """
        return self.measurement_repo.find_by_node(nodo_id, start_date, end_date)