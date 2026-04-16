# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Recopilación automática de dependencias para customtkinter
datas_ctk, binaries_ctk, hidden_ctk = collect_all('customtkinter')

a = Analysis(
    ['src/frontend/main_gui.py'],
    pathex=[],
    binaries=binaries_ctk,
    datas=[
        ('src/frontend', 'src/frontend'), 
        ('src/backend', 'src/backend'),
        ('.env', '.'),  # Incluimos el .env base (opcional, se recomienda tener uno fuera)
    ] + datas_ctk,
    hiddenimports=[
        'groq', 
        'darkdetect', 
        'PIL._tkinter_finder',
        'fitz',           # Requerido por PyMuPDF
        'docx',           # Requerido por python-docx
        'requests'        # Requerido para la comunicación con Groq
    ] + hidden_ctk,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'torch', 
        'transformers', 
        'sentence_transformers', 
        'numpy', 
        'nvidia'
    ], # Excluimos librerías pesadas para reducir el tamaño del .exe
    noarchive=False,
    optimize=1, # Optimización ligera para mejorar la carga
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SmartCVFilter_IAgroq_v2.0', # Nombre actualizado 
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True, # Compresión activa para minimizar los ~120MB
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # Mantiene la interfaz limpia sin ventana de comandos
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)