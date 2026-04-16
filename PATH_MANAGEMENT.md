# 📂 PATH MANAGEMENT - Smart CV Filter

## 📍 Ubicación de Componentes Clave

### 🏗️ Carpeta Maestra (Root de Proyectos)
- **Ruta**: `procesos_seleccion/`
- **Descripción**: Directorio principal autogenerado que agrupa todos los procesos de filtrado.

### 🗄️ Sistema de Persistencia (Basado en Archivos)
- **Reporte de Auditoría (`resumen_proceso.csv`)**: 
  - **Ubicación**: Dentro de la carpeta de cada proceso.
  - **Función**: Sustituye a la antigua base de datos SQL. Almacena de forma permanente el historial de análisis, puntuaciones y motivos de la IA para cada candidato.
- **Respaldo de Requisitos (`descripcion_puesto.txt`)**: 
  - **Ubicación**: Dentro de la carpeta de cada proceso.
  - **Función**: Permite al sistema recordar qué perfil se buscaba al reanudar sesiones antiguas.

### 📁 Organización de Salida (Output)
Dentro de cada subcarpeta de proyecto, los CVs se organizan físicamente en:
- **RECLUTADOS/**: Candidatos aptos (Renombrados por nota).
- **DUDAS/**: Candidatos en revisión.
- **DESCARTADOS/**: Candidatos no aptos.

### 🧠 Modelos de IA
- **Ubicación**: Los pesos del modelo `MiniLM-L12-v2` se gestionan localmente a través de la caché de la librería `sentence-transformers` dentro del entorno virtual.