import json
import sys
from dotenv import load_dotenv

from controllers.catalog_keyclock_api import (
    build_version_summary_report,
    fetch_keycloak_images_in_catalog,
    group_images_by_version_label,
    select_latest_image_per_version,
)

from utils.helper import setup_logging

load_dotenv()
logger = setup_logging()


def main():
    try:
        logger.info(
            "[main] Starting Keycloak Content Stream report for most recent Image"
        )

        keycloak_images_api_data = fetch_keycloak_images_in_catalog()
        images_grouped_by_version = group_images_by_version_label(
            keycloak_images_api_data
        )
        latest_image_per_version = select_latest_image_per_version(
            images_grouped_by_version
        )
        report = build_version_summary_report(latest_image_per_version)

        print(json.dumps(report, indent=2))
        logger.info("[main] Report generation completed successfully")

    except Exception as e:
        logger.error(f"[main] Report generation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
