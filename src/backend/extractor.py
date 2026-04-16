"""
================================================================================
SMART CV FILTER - TEXT EXTRACTION ENGINE (EXTRACTOR)
================================================================================
Author: Tebagl
Date: April 2026
Version: 2.0 (Cloud Migration)

Description:
The low-level extraction layer. This module specializes in deep parsing of 
document structures to recover text from various formats. It acts as the 
bridge between binary files (PDF/DOCX) and the high-level processing pipeline.

TECHNICAL SPECIFICATIONS:
- PDF Parsing: Utilizes PDFMiner.six / PyMuPDF for structural text recovery.
- Word Parsing: Utilizes python-docx for XML-based text extraction.
- Encoding: Forces UTF-8 normalization to prevent character corruption.

KEY RESPONSIBILITIES:
- Format Detection: Identifies file types and routes to the correct parser.
- Layout Preservation: Attempts to maintain logical text flow (crucial for CVs).
- Error Resilience: Handles password-protected or malformed documents 
  without crashing the main application.

DATA OUTPUT:
- Returns a clean, normalized string ready for the AI Analyzer.
================================================================================
"""

import os
import pdfplumber

try:
    import docx
except ImportError:
    docx = None


class CVExtractor:
    """Clase para extraer texto de archivos de CV"""
    def __init__(self):
        pass

    def extract_text(self, file_path):
        """Lee el contenido de un archivo de texto"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error al extraer texto de {file_path}: {e}")
            return ""


class UniversalExtractor:
    """
    Módulo 1: UniversalExtractor
    Soporta extracción de texto de múltiples formatos (.pdf, .docx, .txt).
    Prioriza el uso de pdfplumber y soporta lectura en 2 columnas para PDFs complejos.
    """
    
    @staticmethod
    def extract_text(file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo no existe: {file_path}")
            
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == ".pdf":
            return UniversalExtractor._extract_from_pdf(file_path)
        elif ext == ".docx":
            if docx is None:
                raise ImportError("La librería python-docx no está instalada. Ejecuta 'pip install python-docx'.")
            return UniversalExtractor._extract_from_docx(file_path)
        elif ext in [".txt", ".rtf", ".doc"]:
            # Nota: .doc y .rtf reales requerirían utilidades como antiword o striprtf.
            # Aquí usamos el fallback a lectura en crudo para fines de demostración/simplificación.
            return UniversalExtractor._extract_from_txt(file_path)
        else:
            raise ValueError(f"Formato no soportado: {ext}")

    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """
        Extrae texto de un PDF utilizando pdfplumber.
        Intenta mantener el flujo de lectura adecuado en diseños de 2 columnas
        dividiendo el bounding box de la página a la mitad horizontalmente.
        """
        text_content = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                width = float(page.width)
                height = float(page.height)
                
                # Definir cajas limitadoras: (x0, top, x1, bottom)
                # left_bbox para la columna izquierda, right_bbox para la derecha.
                left_bbox = (0, 0, width / 2, height)
                right_bbox = (width / 2, 0, width, height)
                
                # Recortamos la página en dos partes
                left_page = page.within_bbox(left_bbox)
                right_page = page.within_bbox(right_bbox)
                
                # Extraemos el texto por separado
                left_text = left_page.extract_text(x_tolerance=2, y_tolerance=3)
                right_text = right_page.extract_text(x_tolerance=2, y_tolerance=3)
                
                left_col = left_text.strip() if left_text else ""
                right_col = right_text.strip() if right_text else ""
                
                # Combinamos para un flujo lineal
                combined_text = left_col + "\n" + right_col
                if combined_text.strip():
                    text_content.append(combined_text.strip())
                    
        return "\n\n".join(text_content)

    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """Extrae texto de documentos DOCX."""
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    @staticmethod
    def _extract_from_txt(file_path: str) -> str:
        """Extrae texto de documentos planos TXT."""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

