import json
from typing import List
from dominio import Sintoma
from infraestructura import MotorDeInferencia

def extraer_sintomas_unicos(ruta_json: str) -> List[str]:
    """
    Función de apoyo para extraer dinámicamente todos los síntomas 
    únicos del JSON sin tener que 'quemarlos' en el código (Hardcoding).
    """
    sintomas_unicos = set()
    try:
        with open(ruta_json, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for trastorno in data.get('trastornos', []):
                condiciones = trastorno.get('criterios', {}).get('condiciones', [])
                for cond in condiciones:
                    for sintoma in cond.get('sintomas', []):
                        sintomas_unicos.add(sintoma)
    except Exception as e:
        print(f"Error crítico al leer la base de conocimientos: {e}")
        
    return sorted(list(sintomas_unicos))

def main():
    print("=" * 70)
    print("SISTEMA EXPERTO DE TRIAJE PRE-CLÍNICO (Motor DSM-5)")
    print("=" * 70)
    
    ruta_base = 'base_conocimientos.json'
    nombres_sintomas = extraer_sintomas_unicos(ruta_base)
    
    if not nombres_sintomas:
        print("La base de conocimientos está vacía o es inaccesible. Terminando ejecución.")
        return

    sintomas_paciente = []
    
    print("\nFase de Recolección de Hechos:")
    print("Por favor, responda si el paciente presenta los siguientes síntomas (s/n)")
    print("-" * 70)
    
    #Recolección de datos
    for id_sintoma in nombres_sintomas:
        # Hacemos que el ID (ej: animo_deprimido) sea más legible para el usuario
        nombre_legible = id_sintoma.replace('_', ' ').capitalize()
        
        while True:
            respuesta = input(f"¿Presenta el paciente '{nombre_legible}'? (s/n): ").strip().lower()
            if respuesta in ['s', 'n']:
                break
            print("  [!] Error de entrada. Por favor, ingrese 's' para Sí o 'n' para No.")
            
        presente = (respuesta == 's')
        
        # Mapeamos a nuestra entidad de dominio puro
        sintomas_paciente.append(Sintoma(id_sintoma=id_sintoma, descripcion=nombre_legible, presente=presente))
        
    #Inyección de dependencias y ejecución del motor
    print("\n" + "=" * 70)
    print("EJECUTANDO MOTOR DE INFERENCIA LÓGICA (FORWARD CHAINING)...")
    print("=" * 70)
    
    motor = MotorDeInferencia(ruta_base)
    resultado = motor.evaluar(sintomas_paciente)
    
    #Presentación del Output
    print("\n[ DIAGNÓSTICOS PROBABLES INFERIDOS ]")
    if resultado.trastornos_posibles:
        for trastorno in resultado.trastornos_posibles:
            print(f" -> {trastorno.codigo_dsm5} | {trastorno.nombre} (Confianza: {trastorno.porcentaje_coincidencia}%)")
    else:
        print(" -> [Info] No se infirieron trastornos clínicos que alcancen los criterios mínimos.")
        
    print("\n[ CAPACIDAD DE EXPLICACIÓN: RASTRO DE RAZONAMIENTO ]")
    for paso in resultado.rastro_razonamiento:
        print(paso)
        
    print("\n" + "=" * 70)
    print(resultado.advertencia)
    print("=" * 70)

if __name__ == "__main__":
    main()