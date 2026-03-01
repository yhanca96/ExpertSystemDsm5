from dataclasses import dataclass, field
from typing import List

@dataclass
class Sintoma:
    id_sintoma: str
    descripcion: str
    presente: bool = False

@dataclass
class TrastornoProbable:
    codigo_dsm5: str
    nombre: str
    porcentaje_coincidencia: float

@dataclass
class ResultadoTriaje:
    trastornos_posibles: List[TrastornoProbable] = field(default_factory=list)
    rastro_razonamiento: List[str] = field(default_factory=list) # Capacidad de explicación del Sistema Experto
    advertencia: str = (
        "ADVERTENCIA LEGAL Y CLÍNICA: Este sistema es una herramienta de soporte a la "
        "decisión (CDSS) basada en los criterios del DSM-5. No emite diagnósticos médicos "
        "definitivos y no sustituye la evaluación formal de un profesional de la salud mental."
    )