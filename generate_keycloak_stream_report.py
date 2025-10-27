import json
from dotenv import load_dotenv

from controllers.catalog_keyclock_api import (
    build_version_summary_report,
    fetch_keycloak_images_in_catalog,
    group_images_by_version_label,
    select_latest_image_per_version,
)

load_dotenv()


def main():
    keycloak_images_api_data = fetch_keycloak_images_in_catalog()
    images_grouped_by_version = group_images_by_version_label(keycloak_images_api_data)
    latest_image_per_version = select_latest_image_per_version(
        images_grouped_by_version
    )
    print(json.dumps(build_version_summary_report(latest_image_per_version), indent=2))
    return build_version_summary_report(latest_image_per_version)


if __name__ == "__main__":
    main()
