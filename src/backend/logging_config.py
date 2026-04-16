"""
================================================================================
SMART CV FILTER - CENTRALIZED LOGGING SYSTEM (LOGGING_CONFIG)
================================================================================
Author: Tebagl
Date: April 2026
Version: 2.0 (Cloud Migration)

Description:
The diagnostic heartbeat of the application. It establishes a unified logging 
protocol for both terminal output and persistent file storage, ensuring that 
all modules report errors and events in a standardized format.

KEY FEATURES:
- Dual-Output Logging: Real-time console reporting and file-based archiving.
- Severity Levels: Categorizes events into INFO, WARNING, ERROR, and CRITICAL.
- Traceback Capture: Records detailed error stacks for debugging GUI freezes.
- Timestamping: Precise chronological tracking of the AI analysis workflow.

LOGGING LEVELS:
- INFO: Process starts, file discoveries, and successful API completions.
- WARNING: Missing optional files or non-critical extraction skips.
- ERROR: API connection failures or document corruption.
- CRITICAL: System-level crashes (Segmentation Faults) or missing secrets.

OUTPUT:
- smart_cv_filter.log: The persistent file used for post-mortem analysis.
================================================================================
"""

import os
import logging
import structlog
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional, Union, Dict, Any

class SmartCVFilterLogger:
    """
    Comprehensive logging configuration for Smart CV Filter application.
    Supports structured logging, file and console output, and multiple log levels.
    """
    _instance = None

    def __new__(cls):
        """
        Singleton pattern to ensure a single logger instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self, 
        log_level: str = 'INFO', 
        log_dir: Optional[Union[str, Path]] = None
    ):
        """
        Initialize logging configuration.

        :param log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        :param log_dir: Directory for log files. Defaults to 'logs' in project root
        """
        # Prevent re-initialization
        if hasattr(self, '_initialized'):
            return

        # Detección robusta de la raíz del proyecto
        if log_dir is None:
            # Obtenemos la ruta absoluta del archivo actual
            current_path = Path(__file__).resolve()
            # Subimos 3 niveles: backend -> src -> raiz
            project_root = current_path.parent.parent.parent
            log_dir = project_root / 'logs'

        # Create log directory if it doesn't exist
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        # Convert log level to uppercase
        log_level = log_level.upper()

        # Configure standard logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Configure file handler with rotation
        log_file = log_dir / 'smart_cv_filter.log'
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))

        # Configure console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(name)s - %(levelname)s - %(message)s'
        ))

        # Configure structlog
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        # Get root logger and add handlers
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

        # Mark as initialized
        self._initialized = True

    def get_logger(self, name: str = 'smart_cv_filter') -> structlog.BoundLogger:
        """
        Get a structured logger for a specific component.

        :param name: Logger name (defaults to 'smart_cv_filter')
        :return: Structured logger instance
        """
        return structlog.get_logger(name)

    def log_exception(
        self, 
        logger: Optional[structlog.BoundLogger] = None, 
        message: str = "Unhandled exception occurred",
        extra: Optional[Dict[str, Any]] = None
    ):
        """
        Log an exception with optional additional context.

        :param logger: Optional logger instance
        :param message: Exception message
        :param extra: Additional context dictionary
        """
        import sys
        import traceback

        # Use provided logger or get default
        log = logger or self.get_logger()

        # Log the exception
        log.error(
            message,
            exc_info=sys.exc_info(),
            traceback=traceback.format_exc(),
            **(extra or {})
        )

    def capture_performance_metrics(
        self, 
        operation: str, 
        duration: float, 
        extra: Optional[Dict[str, Any]] = None
    ):
        """
        Log performance metrics for an operation.

        :param operation: Name of the operation
        :param duration: Time taken in seconds
        :param extra: Additional context dictionary
        """
        logger = self.get_logger('performance')
        logger.info(
            "Operation performance",
            operation=operation,
            duration_seconds=duration,
            **(extra or {})
        )

# Global logger instance
logger = SmartCVFilterLogger()

# Decorator for logging function calls and exceptions
def log_function_call(func):
    """
    Decorator to log function entry, exit, and any exceptions.
    """
    import functools
    import time

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        log = logger.get_logger(func.__module__)
        start_time = time.time()
        
        try:
            log.info(
                "Function call started", 
                function=func.__name__, 
                args=args, 
                kwargs=kwargs
            )
            
            result = func(*args, **kwargs)
            
            duration = time.time() - start_time
            logger.capture_performance_metrics(
                func.__name__, 
                duration, 
                {'module': func.__module__}
            )
            
            log.info(
                "Function call completed", 
                function=func.__name__
            )
            
            return result
        
        except Exception as e:
            logger.log_exception(
                log, 
                f"Exception in {func.__name__}", 
                {
                    'function': func.__name__, 
                    'module': func.__module__
                }
            )
            raise

    return wrapper