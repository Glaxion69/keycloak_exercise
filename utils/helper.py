import os
import logging


REDHAT_CATALOG_BASE_URL = os.getenv(
    "REDHAT_CATALOG_BASE_URL", "https://catalog.redhat.com/api/containers/v1"
)

REDHAT_KEYCLOAK_IMAGES_ENDPOINT = f"{REDHAT_CATALOG_BASE_URL}/repositories/registry/registry.access.redhat.com/repository/rhbk%2Fkeycloak-rhel9/images"


def setup_logging():
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
    logger = logging.getLogger(__name__)

    if LOG_LEVEL == "INFO":
        logger.info(
            "Log level set to INFO (default). You can change it via .env (LOG_LEVEL)."
        )
    else:
        logger.debug(f"Logging initialized at {LOG_LEVEL} level.")

    return logger
