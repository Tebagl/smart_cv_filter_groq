# 📑 Smart CV Filter - Historia y Hoja de Ruta

## 🎯 Visión General
Sistema profesional de filtrado y evaluación semántica de CVs. Evolucionado de un modelo 100% local a una **arquitectura de inferencia híbrida ultra-rápida (Groq)**, manteniendo la **privacidad por diseño** mediante anonimización previa en el cliente.

---

## 🕒 Historial de Desarrollo y Log de Versiones

### **Fase 1: Cimientos y Extracción (v0.1 - v0.3)**
* **v0.1 - UniversalExtractor**: Soporte para PDF (pdfplumber), DOCX y TXT.
* **v0.2 - LocalAnonymizer**: Anonimización local mediante spaCy (NER).
* **v0.3 - Calidad**: Suite de tests unitarios y validación de extracción.

### **Fase 2: Orquestación y Transición a la Nube (v0.4 - v0.6)**
* **v0.4 - Orchestrator**: Primer flujo completo de análisis.
* **v0.5 - Era Gemini**: Integración temporal con Google Gemini API.
* **v0.6 - Utilidades**: Scripts de limpieza de entorno y gestión de SQL.

### **Fase 3: IA Local y Gestión de Procesos (v0.7 - v1.4.0)**
* **v1.1.0 - Privacy & Local Update**: Integración de `MiniLM-L12-v2` (100% Local).
* **v1.2.0 - The Organizer Update**: Clasificación física automatizada en carpetas.
* **v1.3.0 - The Precision Update**: Parche de negaciones regex y organización por proyectos.
* **v1.4.0 - Persistence Update**: Generación de `resumen_proceso.csv` y arquitectura `ProcessManager`.

### **Fase 4: Inferencia Ultrarrápida y Formatos Libres (v2.0.0) [ESTADO ACTUAL]**
* **v2.0.0 - The Groq Speed Update**:
    * **Inferencia en la Nube (Groq)**: Migración a la API de Groq (Llama 3) para reducir el tiempo de análisis de minutos a milisegundos.
    * **Soporte ODT**: Implementación de `odfpy` para la lectura nativa de archivos de OpenOffice/LibreOffice.
    * **Optimización de Binarios**: Reducción del ejecutable de 2.5GB a ~120MB al eliminar dependencias pesadas de PyTorch/Transformers.
    * **Compilación Wine**: Estabilización del entorno de empaquetado para Windows 10 desde Linux.

---

## 🏗️ Arquitectura del Sistema (Pipeline)
1.  **Ingestión**: Selección de CVs y detección de formatos (PDF, DOCX, ODT, TXT).
2.  **Anonimización Local**: Sustitución de datos sensibles antes de salir del equipo.
3.  **Inferencia Groq**: Envío de texto anonimizado a la API de Groq para evaluación semántica profunda.
4.  **Logística**: 
    * Clasificación física en `RECLUTADOS/`, `DUDAS/` o `DESCARTADOS/`.
    * Renombrado de archivos por score invertido para ordenamiento automático.
5.  **Trazabilidad**: Actualización del CSV de auditoría y base de datos local.

---

## 🚀 Hoja de Ruta Futura (Roadmap)

### **Próximos Hitos (v2.1 - v2.2)**
- [ ] **Validación Dinámica de API Key**: Interfaz en la GUI para introducir/validar la Key de Groq sin editar el `.env`.
- [ ] **Gestión de Reintentos**: Lógica de *exponential backoff* para manejar límites de ratio en la API.
- [ ] **Dashboard de Estadísticas**: Gráficos de distribución de candidatos integrados en CustomTkinter.

### **Objetivos a Largo Plazo**
- [ ] **Soporte Multi-idioma**: Adaptar el motor de análisis para CVs en inglés, francés y alemán.
- [ ] **Feedback Loop**: Permitir que el reclutador ajuste los umbrales de puntuación en tiempo real desde la GUI.
- [ ] **Pre-visualización**: Integrar un visor de documentos interno para abrir archivos directamente desde la lista de resultados.

---

## 🛠️ Stack Tecnológico Actual
* **Lenguaje**: Python 3.10+ (Entorno Wine para .exe).
* **GUI**: CustomTkinter (Modern Dark Theme).
* **NLP/IA**: Groq SDK (Inferencia), spaCy (Anonimización local).
* **Formatos**: PyMuPDF, python-docx, defusedxml.
* **Persistencia**: CSV (Append), SQLite, Pathlib.

---

## 📝 Principios de Diseño
* **Eficiencia**: Ejecución instantánea sin necesidad de hardware potente (GPU).
* **Privacidad**: Anonimización local garantizada antes de usar servicios de terceros.
* **Portabilidad**: Ejecutable ligero de fácil distribución mediante USB o red.