import logging
from typing import Optional
from opencensus.ext.azure.log_exporter import AzureLogHandler


def configure_application_logger(
    name: str,
    log_level: int = logging.INFO,
    connection_string: Optional[str] = None
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if connection_string:
        handler = AzureLogHandler(connection_string=connection_string)
        logger.addHandler(handler)
    else:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.warning("No Application Insights connection string provided. Logging only to console.")

    return logger