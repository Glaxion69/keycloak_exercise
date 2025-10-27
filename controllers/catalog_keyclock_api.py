import requests
from datetime import datetime
from utils.Exceptions import (
    ApiRespondedNullException,
    ApiResponseUnexpectedFormatException,
    UnexpectedSteamVersionException,
    InvalidImageDataFoundException,
    UnexpectedDateFormat,
)

from utils.helper import (
    setup_logging,
    REDHAT_KEYCLOAK_IMAGES_ENDPOINT,
    REDHAT_CATALOG_BASE_URL,
)

logger = setup_logging()


def fetch_keycloak_images_in_catalog():
    try:
        request_headers = {"accept": "application/json"}
        logger.info(
            f"[fetch_keycloak_images_in_catalog] Fetching Keycloak images from catalog: {REDHAT_CATALOG_BASE_URL}"
        )

        try:
            catalog_response = requests.get(
                REDHAT_KEYCLOAK_IMAGES_ENDPOINT, headers=request_headers
            )
            catalog_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(
                f"[fetch_keycloak_images_in_catalog] Failed to fetch Keycloak images:\nEndpoint: {REDHAT_KEYCLOAK_IMAGES_ENDPOINT}\nError: {e}"
            )
            raise ApiRespondedNullException(REDHAT_KEYCLOAK_IMAGES_ENDPOINT)

        response_json = catalog_response.json()
        if not response_json:
            raise ApiRespondedNullException(REDHAT_KEYCLOAK_IMAGES_ENDPOINT)

        if "data" not in response_json:
            raise ApiResponseUnexpectedFormatException(REDHAT_KEYCLOAK_IMAGES_ENDPOINT)

        return response_json

    except (ApiRespondedNullException, ApiResponseUnexpectedFormatException) as e:
        logger.error(f"[fetch_keycloak_images_in_catalog] API error: {e}")
        raise
    except Exception as e:
        logger.error(f"[fetch_keycloak_images_in_catalog] Unexpected failure: {e}")
        raise


def group_images_by_version_label(api_response_data):
    try:
        logger.info(
            "[group_images_by_version_label] Grouping images by version (Content Streams)"
        )

        images_grouped_by_version = {}

        for image_entry in api_response_data.get("data", []):
            parsed_data_labels = image_entry.get("parsed_data", {}).get("labels", [])
            version_label_value = None

            for label_entry in parsed_data_labels:
                if label_entry.get("name") == "version":
                    version_label_value = label_entry.get("value")
                    break

            if version_label_value:
                if version_label_value not in images_grouped_by_version:
                    images_grouped_by_version[version_label_value] = []
                images_grouped_by_version[version_label_value].append(image_entry)

        if not images_grouped_by_version:
            logger.error(
                "[group_images_by_version_label] No valid version labels found to match Content Stream"
            )
            raise UnexpectedSteamVersionException(
                "version labels", "no images contained valid version information"
            )

        logger.info(
            f"[group_images_by_version_label] Grouped {len(images_grouped_by_version)} unique Content Stream"
        )
        return images_grouped_by_version

    except UnexpectedSteamVersionException as e:
        logger.error(f"[group_images_by_version_label] Content Stream not found: {e}")
        raise
    except Exception as e:
        logger.error(f"[group_images_by_version_label] Unexpected failure: {e}")
        raise


def select_latest_image_per_version(images_grouped_by_version):
    try:
        logger.info(
            "[select_latest_image_per_version] Selecting latest image per Content Stream"
        )

        latest_image_per_version = {}

        for version_label, images_for_version in images_grouped_by_version.items():
            most_recent_image = None
            most_recent_published_date = None

            for image_entry in images_for_version:
                image_repositories = image_entry.get("repositories", [])

                if not image_repositories or not image_repositories[0].get(
                    "published_date"
                ):
                    continue

                try:
                    published_date_string = image_repositories[0]["published_date"]
                    ##Normalize 'Z' suffix for Python 3.7-3.10 compatibility
                    normalized_date_string = published_date_string.replace(
                        "Z", "+00:00"
                    )
                    current_published_date = datetime.fromisoformat(
                        normalized_date_string
                    )

                    if (
                        most_recent_published_date is None
                        or current_published_date > most_recent_published_date
                    ):
                        most_recent_published_date = current_published_date
                        most_recent_image = image_entry

                except ValueError as e:
                    logger.warning(
                        f"[select_latest_image_per_version] Skipping image with invalid date format for Content Stream '{version_label}': {published_date_string}"
                    )
                    raise UnexpectedDateFormat(published_date_string, version_label)

            if most_recent_image:
                latest_image_per_version[version_label] = most_recent_image
            else:
                logger.warning(
                    f"[select_latest_image_per_version] No valid images found for Content Stream '{version_label}'"
                )

        if not latest_image_per_version:
            logger.error(
                "[select_latest_image_per_version] No valid images found across all Streams"
            )
            raise InvalidImageDataFoundException(
                "image had invalid or missing date information"
            )
        return latest_image_per_version

    except (UnexpectedDateFormat, InvalidImageDataFoundException) as e:
        logger.error(f"[select_latest_image_per_version] No image Data found: {e}")
        raise
    except Exception as e:
        logger.error(f"[select_latest_image_per_version] Unexpected failure: {e}")
        raise


def build_version_summary_report(latest_image_per_version):
    try:
        logger.info("[build_version_summary_report] Building version summary report")

        if not latest_image_per_version:
            logger.error("[build_version_summary_report] No image data to build report")
            raise InvalidImageDataFoundException(
                "no image data provided for report generation"
            )

        version_summary_report = []

        for version_label, image_data in latest_image_per_version.items():
            parsed_data_labels = image_data.get("parsed_data", {}).get("labels", [])
            vcs_ref_value = None

            for label_entry in parsed_data_labels:
                if label_entry.get("name") == "vcs-ref":
                    vcs_ref_value = label_entry.get("value")
                    break

            image_repositories = image_data.get("repositories", [])
            published_date_string = (
                image_repositories[0].get("published_date")
                if image_repositories
                else None
            )

            image_freshness_grades = image_data.get("freshness_grades", [])
            freshness_grade_value = (
                image_freshness_grades[0].get("grade")
                if image_freshness_grades
                else None
            )

            version_summary_report.append(
                {
                    "contentStream": version_label,
                    "vcsRef": vcs_ref_value,
                    "publishedDate": published_date_string,
                    "freshnessGrade": freshness_grade_value,
                }
            )

        logger.info(
            f"[build_version_summary_report] Successfully built report with {len(version_summary_report)} entries"
        )
        return version_summary_report

    except InvalidImageDataFoundException as e:
        logger.error(f"[build_version_summary_report] No image data found: {e}")
        raise
    except Exception as e:
        logger.error(f"[build_version_summary_report] Unexpected failure: {e}")
        raise
