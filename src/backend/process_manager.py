"""
================================================================================
SMART CV FILTER - WORKFLOW & STORAGE MANAGER (PROCESS_MANAGER)
================================================================================
Author: Tebagl
Date: April 2026
Version: 2.0 (Cloud Migration)

Description:
The administrative core of the application. It manages the lifecycle of each 
recruitment process, handling directory structures, file naming conventions, 
and the persistent storage of results in CSV format.

KEY RESPONSIBILITIES:
- Session Management: Creates and resumes time-stamped project folders.
- File Synchronization: Maps original CVs to their analyzed counterparts.
- Data Persistence: Manages the 'resumen_proceso.csv' state to ensure no 
  analysis is lost during app restarts.
- Path Normalization: Ensures cross-platform compatibility for file operations.

ORGANIZATIONAL STRUCTURE:
Procesos/
└── YYYY-MM-DD_ProjectName/
    ├── resumen_proceso.csv      # Detailed AI scores, reasons, and analysis results.
    ├── job_description.txt      # Reference text used for the screening criteria.
    └── [Copied_CVs]/            # Local copy of processed documents for audit and backup.

STABILITY FEATURES:
- Automatic folder creation (atomic operations).
- Duplicate detection to prevent re-analyzing the same file.
- Safe closing of file handles to prevent data corruption.
================================================================================
"""

import os
import platform
import ctypes
from datetime import datetime

def hide_folder(path):
    """
    Oculta una carpeta en Windows añadiendo el atributo de sistema 'Hidden'.
    En otros sistemas operativos no realiza ninguna acción para evitar errores.
    """
    if platform.system() == "Windows":
        try:
            # Atributo 2 corresponde a FILE_ATTRIBUTE_HIDDEN
            ctypes.windll.kernel32.SetFileAttributesW(str(path), 2)
        except Exception:
            pass

class ProcessManager:
    def __init__(self, base_path, cv_handler):
        self.base_path = base_path
        self.cv_handler = cv_handler
        # 🛡️ Limpiamos la interfaz visual nada más arrancar
        self.cleanup_ui_folders()


    def cleanup_ui_folders(self):
        """Oculta las carpetas técnicas para que el usuario final no se abrume."""
        to_hide = [
            "src",
            "logs",
            "models",
            "build",
            "ai-specs",
            "openspec",
            "Procesos",  # Carpeta antigua por si acaso
            "__pycache__",
            ".cursor",
            ".roo"
        ]
        
        for folder_name in to_hide:
            folder_path = os.path.join(self.base_path, folder_name)
            if os.path.exists(folder_path):
                hide_folder(folder_path)

 
    def configure_process(self, puesto, ruta_seleccionada):
        """
        Configura las rutas respetando la fecha original del proceso si ya existe.
        """
        # 1. Definimos los indicadores de estructura
        indicadores = ["RECLUTADOS", "DESCARTADOS", "DUDAS"]
        
        # Comprobamos si el usuario ha seleccionado una carpeta que ya es un proceso
        es_proceso_existente = all(
            os.path.isdir(os.path.join(ruta_seleccionada, f)) for f in indicadores
        )

        if es_proceso_existente:
            # ♻️ CONTINUAR: Mantenemos la ruta exacta que el usuario eligió.
            # No se toca el nombre, por lo tanto, la fecha original se mantiene intacta.
            ruta_proceso = ruta_seleccionada
            print(f"♻️ Continuando proceso original en: {os.path.basename(ruta_proceso)}")
        else:
            # ✨ NUEVO: Aquí sí generamos la fecha de creación única.
            fecha_creacion = datetime.now().strftime("%Y-%m-%d")
            nombre_carpeta = f"{fecha_creacion}_{puesto.replace(' ', '_')}"
            
            ruta_proceso = os.path.join(ruta_seleccionada, nombre_carpeta)
            print(f"✨ Creando nuevo proceso con fecha de hoy: {nombre_carpeta}")

        # 2. Sincronizar con el Handler y asegurar carpetas
        self.cv_handler.base_output = ruta_proceso 
        self.cv_handler._ensure_folders()
        
        self.cleanup_ui_folders()
        
        ruta_reclutados = os.path.join(ruta_proceso, "RECLUTADOS")
        return ruta_proceso, ruta_reclutados
    


    def save_job_description(self, folder_path, description):
       """Guarda la descripción del puesto en un archivo de texto dentro de la carpeta del proceso."""
       try:
           file_path = os.path.join(folder_path, "descripcion_puesto.txt")
           with open(file_path, "w", encoding="utf-8") as f:
               f.write(description)
           return True
       except Exception as e:
           print(f"Error al guardar la descripción: {e}")
           return False