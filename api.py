from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import dataclasses

from dominio import Sintoma
from infraestructura import MotorDeInferencia

# 1. Configuración de la API
app = FastAPI(
    title="API Sistema Experto DSM-5",
    description="Motor de Inferencia Forward Chaining para Triaje Clínico",
    version="1.0.0"
)

# 2. Configuración CORS (Crucial para que tu Frontend en React/HTML pueda comunicarse con esta API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción esto se cambia por el dominio real de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Inyección de la dependencia del motor
motor = MotorDeInferencia('base_conocimientos.json')

# 4. DTO (Data Transfer Object) para la entrada web
class SintomaInput(BaseModel):
    id_sintoma: str
    presente: bool

# 5. Endpoints
@app.get("/")
def ruta_raiz():
    """Ruta de comprobación de estado de la API."""
    return {
        "mensaje": "Bienvenido a la API del Sistema Experto DSM-5",
        "estado": "En linea",
        "documentacion": "Visita http://127.0.0.1:8000/docs para probar el sistema"
    }

@app.post("/api/evaluar")
def evaluar_paciente(sintomas_request: List[SintomaInput]):
    """
    Recibe una lista de síntomas, evalúa las reglas clínicas del DSM-5 
    y devuelve los posibles trastornos junto con el rastro de razonamiento.
    """
    # Mapeamos los datos web a nuestras entidades de dominio puro
    sintomas_dominio = []
    for sint in sintomas_request:
        sintomas_dominio.append(
            Sintoma(
                id_sintoma=sint.id_sintoma, 
                descripcion=sint.id_sintoma.replace('_', ' ').title(), 
                presente=sint.presente
            )
        )
    
    # El motor ejecuta el Forward Chaining
    resultado = motor.evaluar(sintomas_dominio)
    
    # Transformamos nuestra Dataclass a Diccionario estándar para evitar el Error 500
    return dataclasses.asdict(resultado)