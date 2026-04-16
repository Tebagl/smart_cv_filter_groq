## 🚀 Hoja de Ruta Futura (Roadmap)

### **Próximos Hitos (v1.4 - v1.5)**
- [ ] **Refactorización (ProcessManager)**: Separar completamente la lógica de creación de carpetas de la interfaz de usuario.
- [ ] **Empaquetado Final**: Generación de ejecutable `.exe` único incluyendo los pesos del modelo de IA.
- [ ] **Exportación de Reportes**: Generar un archivo CSV resumen con el ranking y motivos dentro de cada carpeta de proceso.
- [ ] **Lazy Loading**: Carga asíncrona del modelo de IA para que la ventana abra instantáneamente.

### **Objetivos a Largo Plazo**
- [ ] **Soporte Multi-idioma**: Adaptar el motor de negaciones para CVs en inglés.
- [ ] **Feedback Loop**: Permitir que el reclutador ajuste los umbrales de puntuación desde la GUI.
- [ ] **Pre-visualización**: Abrir el CV analizado directamente desde la lista de la interfaz.

---

## 🛠️ Stack Tecnológico Actual
* **Lenguaje**: Python 3.10+
* **GUI**: CustomTkinter (Modern Dark Theme).
* **NLP/AI**: spaCy, sentence-transformers, PyTorch (All Local).
* **Documentos**: PyMuPDF (fitz), python-docx.
* **Logística**: Shutil, Pathlib.

---

## 📝 Principios de Diseño
* **Privacidad**: El dato nunca sale del ordenador del usuario.
* **Orden**: El sistema no solo analiza, sino que organiza el caos documental.
* **Transparencia**: El "Motivo" de la IA siempre es visible para el reclutador.

# 📑 Smart CV Filter - Historia y Hoja de Ruta

## 🎯 Visión General
Sistema profesional de filtrado y evaluación semántica de CVs que prioriza la **privacidad por diseño** y el **procesamiento local**. Utiliza técnicas avanzadas de NLP y Embeddings para emparejar perfiles candidatos con descripciones de puestos (Job Descriptions) sin enviar datos sensibles a la nube.

---

## 🕒 Historial de Desarrollo y Log de Versiones

### **Fase 1: Cimientos y Extracción (v0.1 - v0.3)**
* **v0.1 - UniversalExtractor**: Soporte para PDF (pdfplumber), DOCX y TXT.
* **v0.2 - LocalAnonymizer**: Anonimización local mediante spaCy (NER).
* **v0.3 - Calidad**: Suite de tests unitarios y validación de extracción.

### **Fase 2: Orquestación y Transición a la Nube (v0.4 - v0.6)**
* **v0.4 - Orchestrator**: Primer flujo completo de análisis.
* **v0.5 - Era Gemini**: Integración temporal con Google Gemini API para validación de rúbricas.
* **v0.6 - Utilidades**: Scripts de limpieza de entorno y gestión de base de datos SQL.

### **Fase 3: IA Local y Gestión de Procesos (v0.7 - v1.4.0) [ESTADO ACTUAL]**
* **v1.1.0 - Privacy & Local Update**: Eliminación total de APIs externas. Integración de `MiniLM-L12-v2`.
* **v1.2.0 - The Organizer Update**: Clasificación física automatizada en carpetas.
* **v1.3.0 - The Precision & Project Update**: Parche de negaciones regex y organización por proyectos.
* **v1.4.0 - Persistence & Stability Update (Actual)**:
    * **Módulo de Reportes**: Generación automática de `resumen_proceso.csv` para auditoría y trazabilidad del reclutador.
    * **Arquitectura ProcessManager**: Desacoplamiento total de la lógica de archivos; creación automática de la carpeta maestra `procesos_seleccion`.
    * **Memoria de Sesión**: Capacidad de reanudar procesos antiguos cargando automáticamente Fecha, Puesto y Descripción (JD) desde el disco.
    * **Linux Stability**: Optimización del motor gráfico para evitar *Segmentation Faults* mediante carga diferida de temas.

---

## 🏗️ Arquitectura del Sistema (Pipeline)
1.  **Ingestión**: Selección de carpeta de CVs y validación de campos obligatorios.
2.  **Entorno de Proceso**: El `ProcessManager` crea o recupera la estructura de carpetas y carga metadatos previos.
3.  **Limpieza Semántica**: Detección de negaciones y anonimización de datos sensibles.
4.  **Evaluación Local**: Cálculo de similitud del coseno mediante Embeddings locales.
5.  **Logística y Registro**: 
    * Movimiento físico de archivos con renombrado por score.
    * Escritura en el log de auditoría CSV.
    * Sincronización en tiempo real de la lista de candidatos "Estrella" en la GUI.

---

## 🚀 Hoja de Ruta Futura (Roadmap)

### **Próximos Hitos (v1.5 - v1.6)**
- [ ] **Empaquetado Final**: Generación de ejecutable `.exe` / Binario Linux incluyendo los pesos del modelo de IA (PyInstaller).
- [ ] **Lazy Loading**: Carga asíncrona del modelo de IA para que la ventana abra instantáneamente sin bloqueo inicial.
- [ ] **Dashboard de Estadísticas**: Gráficos simples en la GUI sobre la distribución de candidatos (Aptos vs Descartados).

### **Objetivos a Largo Plazo**
- [ ] **Soporte Multi-idioma**: Adaptar el motor de negaciones para CVs en inglés y francés.
- [ ] **Feedback Loop**: Permitir que el reclutador ajuste los umbrales de puntuación ($Threshold$) desde la GUI en tiempo real.
- [ ] **Pre-visualización**: Integrar un visor de PDF interno para abrir el CV analizado directamente desde la lista de la interfaz.

---

## 🛠️ Stack Tecnológico Actual
* **Lenguaje**: Python 3.10+ (Entorno Virtual .venv).
* **GUI**: CustomTkinter (Modern Dark Theme con corrección para Linux).
* **NLP/AI**: spaCy, sentence-transformers (All Local).
* **Persistencia**: CSV (Append mode), Pathlib, Shutil.
* **Sistemas Soportados**: Windows y Linux (X11).

---

## 📝 Principios de Diseño
* **Privacidad**: El dato nunca sale del ordenador del usuario.
* **Continuidad**: El trabajo nunca se pierde; los procesos son reanudables y auditables.
* **Transparencia**: El reclutador siempre sabe el "porqué" de la decisión de la IA a través del CSV y el Log.