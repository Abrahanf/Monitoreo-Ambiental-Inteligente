# ia-service/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import joblib
import numpy as np
from datetime import datetime
import os

app = FastAPI(title="Environmental Monitoring IA Service")

# Modelo global
current_model = None
model_info = {
    'version': '1.0.0',
    'precision': 0.0,
    'sensibilidad': 0.5,
    'loaded': False
}

class MeasurementData(BaseModel):
    nodo_id: int
    temperatura: float
    humedad: float
    co2: float

class TrainingRequest(BaseModel):
    dataset_path: str
    parameters: Optional[dict] = None

class PredictionResponse(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    prediction: dict

@app.on_event("startup")
async def startup_event():
    """Carga el modelo al iniciar"""
    load_model()

def load_model():
    """Carga el modelo de ML"""
    global current_model, model_info
    
    model_path = 'saved_models/anomaly_detector.pkl'
    if os.path.exists(model_path):
        try:
            current_model = joblib.load(model_path)
            model_info['loaded'] = True
            model_info['precision'] = 0.85  # TODO: Cargar desde metadata
            print(f"✓ Modelo cargado: {model_path}")
        except Exception as e:
            print(f"Error cargando modelo: {e}")
    else:
        print("⚠ No hay modelo entrenado. Usando detección basada en reglas.")

@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "service": "Environmental Monitoring IA",
        "status": "running",
        "model_loaded": model_info['loaded']
    }

@app.get("/health")
def health_check():
    """Health check"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/model/info")
def get_model_info():
    """Obtiene información del modelo actual"""
    return model_info

@app.put("/api/model/sensitivity")
def update_sensitivity(data: dict):
    """Actualiza la sensibilidad del modelo"""
    sensitivity = data.get('sensitivity', 0.5)
    
    if not 0 <= sensitivity <= 1:
        raise HTTPException(400, "La sensibilidad debe estar entre 0 y 1")
    
    model_info['sensibilidad'] = sensitivity
    return {"message": "Sensibilidad actualizada", "sensitivity": sensitivity}

@app.post("/api/analyze", response_model=PredictionResponse)
def analyze_measurement(data: MeasurementData):
    """Analiza una medición y detecta anomalías"""
    try:
        # Preparar datos
        features = np.array([[
            data.temperatura,
            data.humedad,
            data.co2
        ]])
        
        if current_model and model_info['loaded']:
            # Usar modelo ML
            anomaly_score = current_model.decision_function(features)[0]
            is_anomaly = current_model.predict(features)[0] == -1
        else:
            # Detección basada en reglas (fallback)
            is_anomaly, anomaly_score = rule_based_detection(data)
        
        # Ajustar con sensibilidad
        threshold = -0.5 + (model_info['sensibilidad'] * 0.5)
        is_anomaly = anomaly_score < threshold
        
        return PredictionResponse(
            is_anomaly=bool(is_anomaly),
            anomaly_score=float(anomaly_score),
            prediction={
                'temperatura_normal': 18 <= data.temperatura <= 26,
                'humedad_normal': 30 <= data.humedad <= 70,
                'co2_normal': 300 <= data.co2 <= 1000
            }
        )
    
    except Exception as e:
        raise HTTPException(500, f"Error en análisis: {str(e)}")

def rule_based_detection(data: MeasurementData):
    """Detección basada en reglas (sin ML)"""
    anomalies = 0
    
    # Verificar rangos normales
    if not (18 <= data.temperatura <= 26):
        anomalies += 1
    if not (30 <= data.humedad <= 70):
        anomalies += 1
    if not (300 <= data.co2 <= 1000):
        anomalies += 1
    
    is_anomaly = anomalies >= 1
    anomaly_score = -anomalies / 3.0  # Score entre 0 y -1
    
    return is_anomaly, anomaly_score

@app.post("/api/train")
def train_model(request: TrainingRequest):
    """Entrena un nuevo modelo"""
    try:
        import pandas as pd
        from sklearn.ensemble import IsolationForest
        
        # Cargar dataset
        if not os.path.exists(request.dataset_path):
            raise HTTPException(404, "Dataset no encontrado")
        
        df = pd.read_csv(request.dataset_path)
        
        # Validar columnas
        required_cols = ['temperatura', 'humedad', 'co2']
        if not all(col in df.columns for col in required_cols):
            raise HTTPException(400, f"El dataset debe contener: {required_cols}")
        
        # Preparar datos
        X = df[required_cols].values
        
        # Parámetros
        params = request.parameters or {}
        contamination = params.get('contamination', 0.1)
        n_estimators = params.get('n_estimators', 100)
        
        # Entrenar modelo
        model = IsolationForest(
            contamination=contamination,
            n_estimators=n_estimators,
            random_state=42
        )
        model.fit(X)
        
        # Guardar modelo
        os.makedirs('saved_models', exist_ok=True)
        model_path = f'saved_models/anomaly_detector.pkl'
        joblib.dump(model, model_path)
        
        # Actualizar modelo global
        global current_model
        current_model = model
        model_info['loaded'] = True
        model_info['version'] = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        model_info['precision'] = 0.85  # TODO: Calcular precisión real
        
        return {
            "message": "Modelo entrenado exitosamente",
            "version": model_info['version'],
            "samples": len(X)
        }
    
    except Exception as e:
        raise HTTPException(500, f"Error entrenando modelo: {str(e)}")

@app.post("/api/batch-analyze")
def batch_analyze(measurements: List[MeasurementData]):
    """Analiza múltiples mediciones"""
    results = []
    
    for measurement in measurements:
        try:
            result = analyze_measurement(measurement)
            results.append({
                'nodo_id': measurement.nodo_id,
                'is_anomaly': result.is_anomaly,
                'anomaly_score': result.anomaly_score
            })
        except Exception as e:
            results.append({
                'nodo_id': measurement.nodo_id,
                'error': str(e)
            })
    
    return {"results": results, "total": len(measurements)}


