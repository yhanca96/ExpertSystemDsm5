DSM-5 Expert System: Triaje Pre-Clínico 🩺
Este proyecto es un Sistema Experto de inteligencia artificial simbólica diseñado para el triaje pre-clínico de trastornos mentales comunes, basado estrictamente en los criterios del manual DSM-5.

Utiliza un Motor de Inferencia de Encadenamiento hacia Adelante (Forward Chaining) para evaluar hechos (síntomas) y derivar conclusiones diagnósticas con capacidad de explicabilidad.

⚠️ NOTA IMPORTANTE (Lectura Obligatoria para el Demo)
Debido a que el backend está alojado en una instancia gratuita de Render, el servidor entra en estado de suspensión tras 15 minutos de inactividad.

Para usar la aplicación correctamente, siga estos pasos:

Ingrese primero a la URL de la API: https://expertsystemdsm5.onrender.com/

Espere unos 30-50 segundos a que aparezca el mensaje de "Bienvenido". Esto "despertará" el motor de inferencia.

Una vez activada la API, podrá usar el Frontend sin retardos: https://yhanca96.github.io/ExpertSystemDsm5/

🏗️ Arquitectura del Sistema
El software ha sido desarrollado bajo los principios de Clean Architecture y SOLID, garantizando un bajo acoplamiento y una alta cohesión entre sus componentes.

Capa de Dominio: Define las entidades puras como Sintoma y Trastorno, independientes de cualquier framework.

Capa de Infraestructura: Aloja el Motor de Inferencia que procesa la lógica booleana recursiva (AND, AT_LEAST).

Base de Conocimientos (KB): El conocimiento clínico está externalizado en un archivo JSON, permitiendo actualizaciones sin modificar el código fuente.

Capa de Presentación (API): Implementada con FastAPI, exponiendo un contrato REST profesional documentado con Swagger UI.

🧠 Motor de Inferencia y Explicabilidad
A diferencia de los sistemas de "caja negra", este motor implementa Explainability (Explicabilidad). Por cada diagnóstico inferido, el sistema devuelve un "Rastro de Razonamiento" que detalla:

Qué síntomas fueron detectados.

Qué reglas lógicas se cumplieron.

Qué criterios faltaron para descartar otras hipótesis.

🛠️ Tecnologías Utilizadas
Backend: Python 3.x, FastAPI, Uvicorn.

Frontend: HTML5, Vanilla JavaScript (Fetch API), Tailwind CSS.

Despliegue: Render (PaaS) y GitHub Pages.

📁 Estructura del Proyecto
api.py: Controlador de la API y configuración de CORS.

infraestructura.py: Lógica del Motor de Inferencia (Forward Chaining).

dominio.py: Modelos de datos y entidades.

base_conocimientos.json: Reglas diagnósticas modeladas del DSM-5.

index.html: Interfaz de usuario reactiva y visual.

🚀 Instalación Local
Si desea ejecutar el proyecto en su máquina:

Clonar el repositorio.

Instalar dependencias: pip install -r requirements.txt.

Iniciar el servidor: python -m uvicorn api:app --reload.

Abrir el archivo index.html en el navegador.

Desarrollado por: 
Yhann Camilo Carmona Usme
Samuel Andrés García Sierra
David Zuluaga Ceballos
Estudiante de Desarrollo de Software - Institución Universitaria ITM
