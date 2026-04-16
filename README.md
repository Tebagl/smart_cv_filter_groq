# 🚀 Smart CV Filter - Cloud Edition (Groq Llama-3)

**Smart CV Filter** es una herramienta de reclutamiento inteligente diseñada para automatizar el cribado inicial de currículums con extrema velocidad y precisión. 

Al aprovechar la tecnología **Groq LPU™ (Language Processing Unit)** y los modelos **Llama 3.1**, esta versión elimina los cuellos de botella de hardware de los LLM locales, procesando docenas de CV en segundos en lugar de horas.

---

## ✨ Características Principales

* **Inferencia Ultra-Rápida:** Potenciado por la API de Groq Cloud para un análisis casi instantáneo.
* **Puntuación Inteligente:** Emparejamiento semántico avanzado entre Descripciones de Puesto y Currículums.
* **Flujo de Trabajo Continuo:** Detecta automáticamente carpetas de proyectos existentes para retomar procesos de selección previos.
* **Reportes Auditables:** Genera archivos `resumen_proceso.csv` detallados con puntuaciones y el razonamiento técnico detrás de cada decisión.
* **Eficiencia de Recursos:** Funciona con fluidez en máquinas con recursos limitados (4GB/8GB RAM) al delegar el procesamiento de IA a la nube.

---

## 🛠️ Tech Stack

* **Lenguaje:** Python 3.x
* **Frontend:** CustomTkinter (Desktop GUI moderna)
* **Motor de IA:** Groq Cloud API (`llama-3.1-8b-instant`)
* **Manejo de Datos:** PDFMiner / PyMuPDF / python-docx / CSV

---

## ⚙️ Guía de Inicio Rápido

### 1. Requisitos Previos
* Una cuenta en [console.groq.com](https://console.groq.com) para obtener tu API Key gratuita.
* Conexión a internet.

### 2. Instalación
```bash
# Clonar el repositorio
git clone [https://github.com/Tebagl/smart_cv_filter_groq.git](https://github.com/Tebagl/smart_cv_filter_groq.git)

# Instalar dependencias
pip install customtkinter python-dotenv requests pdfminer.six python-docx PyMuPDF
```

### 3. Configuración
Crea un archivo `.env` en la raíz del proyecto y añade tu clave:

```env
GROQ_API_KEY=tu_clave_aqui_gsk_...
```

### 4. Ejecución

```bash
python src/frontend/main_gui.py
```
# 📖 Instrucciones de Uso

### Configuración del Proyecto
Define el nombre del puesto y la carpeta de destino donde se guardarán los resultados.

### Carga de Documentos
Selecciona la carpeta que contiene los CVs en formato PDF o DOCX.

### Análisis Semántico
Pega los requisitos o la descripción del puesto y pulsa "**🚀 CLASIFICAR CVS**".

### Gestión de Candidatos
Visualiza los resultados en tiempo real y abre los archivos de los candidatos aceptados directamente desde la lista de la interfaz.

---

# 📂 Arquitectura de Almacenamiento
El sistema garantiza la trazabilidad organizando cada proceso de forma autónoma:

```text
Procesos/
└── YYYY-MM-DD_NombreProyecto/
    ├── job_description.txt      # Respaldo de los requisitos utilizados.
    ├── resumen_proceso.csv      # Informe con puntuaciones y motivos de la IA.
    └── [Copied_CVs]/            # Copia local de los documentos analizados.
```

# 🛠️ Documentación de Módulos (Cabeceras Técnicas)

## 🖥️ Frontend (`src/frontend/`)

* **`main_gui.py`**: Gestión de la interfaz de usuario (UX) y control de hilos asíncronos (*Queues*) para evitar bloqueos durante el análisis. Incluye un parche de estabilidad para Linux/Wayland mediante el forzado de `GDK_BACKEND=x11`.

## 🧠 Backend (`src/backend/`)

* **`analyzer.py`**: Motor de inteligencia. Gestiona peticiones HTTPS a Groq con un prompt determinista (Temperature 0.0).
* **`process_manager.py`**: Director de orquesta. Maneja la creación de directorios, persistencia en CSV y gestión de copias de seguridad.
* **`extractor.py`**: Especialista en *parsing*. Convierte archivos binarios (PDF/Word) en texto plano normalizado en UTF-8.
* **`cv_handler.py`**: Lógica de pre-procesamiento. Limpia caracteres especiales y optimiza el texto para minimizar el uso de tokens.
* **`logging_config.py`**: Sistema de diagnóstico. Centraliza errores y eventos en `smart_cv_filter.log`.


# 🔒 Privacidad y Seguridad

* **Cifrado en Tránsito:** El flujo de datos entre el cliente y el servidor de inferencia viaja cifrado vía HTTPS.
* **Filosofía Local-First:** Aunque el análisis es Cloud, los resultados, logs y copias de seguridad residen exclusivamente en el hardware del usuario.
* **Política de Datos:** Los datos enviados no se utilizan para el entrenamiento de modelos de terceros, respetando la privacidad del candidato.

---
> **Smart CV Filter** - *Transformando el reclutamiento con IA Ética, Rápida y Profesional.*