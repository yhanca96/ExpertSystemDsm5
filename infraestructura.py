import json
from typing import List, Tuple
from dominio import Sintoma, TrastornoProbable, ResultadoTriaje

class MotorDeInferencia:
    def __init__(self, ruta_json: str = 'base_conocimientos.json'):
        self.ruta_json = ruta_json
        self.conocimiento = self._cargar_conocimiento()
        self.rastro = []

    def _cargar_conocimiento(self) -> dict:
        """Carga las reglas del DSM-5 desde el archivo JSON."""
        try:
            with open(self.ruta_json, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"Error: No se encontró el archivo de base de conocimientos '{self.ruta_json}'")
        except json.JSONDecodeError:
            raise Exception(f"Error: El archivo '{self.ruta_json}' no tiene un formato JSON válido.")

    def evaluar(self, sintomas_paciente: List[Sintoma]) -> ResultadoTriaje:
        """
        Función principal (Forward Chaining). 
        Recibe los síntomas, evalúa las reglas y devuelve un ResultadoTriaje.
        """
        self.rastro.clear()
        
        #Filtramos solo los IDs de los síntomas que el paciente SÍ tiene
        sintomas_activos = set(s.id_sintoma for s in sintomas_paciente if s.presente)
        trastornos_posibles = []
        
        self.rastro.append(f"INICIO: Evaluando paciente con {len(sintomas_activos)} síntomas activos.")

        #Iteramos sobre cada trastorno en nuestra base de conocimientos
        for trastorno in self.conocimiento.get('trastornos', []):
            nombre_trastorno = trastorno['nombre']
            codigo_dsm5 = trastorno['codigo_dsm5']
            criterios = trastorno['criterios']
            
            self.rastro.append(f"\n--- Analizando: {nombre_trastorno} ({codigo_dsm5}) ---")
            
            #Llamada recursiva para evaluar el árbol de condiciones lógicas
            cumple_criterios, porcentaje = self._evaluar_nodo(criterios, sintomas_activos)
            
            #Si cumple los criterios, se agrega a los diagnósticos probables
            if cumple_criterios:
                self.rastro.append(f">>> ALERTA CLÍNICA: Se cumplen los criterios para {nombre_trastorno} <<<")
                trastornos_posibles.append(TrastornoProbable(codigo_dsm5, nombre_trastorno, porcentaje))
            else:
                self.rastro.append(f"> Descartado: No alcanza los criterios mínimos. (Nivel de coincidencia: {porcentaje}%)")

        # Devolvemos el objeto de dominio puro
        return ResultadoTriaje(
            trastornos_posibles=trastornos_posibles,
            rastro_razonamiento=self.rastro.copy()
        )

    def _evaluar_nodo(self, nodo: dict, sintomas_activos: set) -> Tuple[bool, float]:
        """
        Evaluador recursivo del Árbol de Sintaxis Abstracta (AST) del JSON.
        Retorna una tupla: (Bool si cumple la regla, Float con porcentaje de coincidencia)
        """
        operador = nodo.get("operador")
        
        if operador == "AND":
            condiciones = nodo.get("condiciones", [])
            cumplidas = 0
            suma_porcentajes = 0
            
            for cond in condiciones:
                cumple, porc = self._evaluar_nodo(cond, sintomas_activos)
                if cumple:
                    cumplidas += 1
                suma_porcentajes += porc
            
            # Para que un AND sea True, se deben cumplir todas las sub-condiciones
            exito = (cumplidas == len(condiciones))
            porcentaje_final = suma_porcentajes / len(condiciones) if condiciones else 0
            
            self.rastro.append(f"  [Operador AND] Se cumplieron {cumplidas} de {len(condiciones)} bloques requeridos.")
            return exito, round(porcentaje_final, 2)
            
        elif operador == "AT_LEAST":
            requeridos = nodo.get("cantidad", 1)
            sintomas_rama = set(nodo.get("sintomas", []))
            
            # Intersección de conjuntos: ¿Qué síntomas de esta regla tiene el paciente?
            coincidencias = sintomas_rama.intersection(sintomas_activos)
            cantidad_coincidencias = len(coincidencias)
            
            exito = (cantidad_coincidencias >= requeridos)
            
            porcentaje = (cantidad_coincidencias / requeridos) * 100
            if porcentaje > 100: porcentaje = 100.0 # Tope máximo de 100%
            
            if exito:
                self.rastro.append(f"    - [Regla AT_LEAST] ÉXITO: Exige {requeridos}, paciente presenta {cantidad_coincidencias}. {list(coincidencias)}")
            else:
                self.rastro.append(f"    - [Regla AT_LEAST] FALLO: Exige {requeridos}, paciente presenta {cantidad_coincidencias}.")
                
            return exito, round(porcentaje, 2)
        
        return False, 0.0