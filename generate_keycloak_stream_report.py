import requests
from datetime import datetime
import json

REDHAT_KEYCLOAK_IMAGES_URL = "https://catalog.redhat.com/api/containers/v1/repositories/registry/registry.access.redhat.com/repository/rhbk%2Fkeycloak-rhel9/images"


def fetch_keycloak_images_in_catalog():
    request_headers = {"accept": "application/json"}
    request_response = requests.get(REDHAT_KEYCLOAK_IMAGES_URL, headers=request_headers)
    request_response.raise_for_status()
    return request_response.json()


def group_images_by_version_label(api_response_data):
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

    return images_grouped_by_version

def select_latest_image_per_version(images_grouped_by_version):
    latest_image_per_version = {}

    for version_label, images_for_version in images_grouped_by_version.items():
        most_recent_image = None
        most_recent_published_date = None

        for image_entry in images_for_version:
            image_repositories = image_entry.get("repositories", [])

            if not image_repositories or not image_repositories[0].get("published_date"):
                continue

            published_date_string = image_repositories[0]["published_date"]
            normalized_date_string = published_date_string.replace("Z","+00:00")
            current_published_date = datetime.fromisoformat(normalized_date_string)

            if most_recent_published_date is None or current_published_date > most_recent_published_date:
                most_recent_published_date = current_published_date
                most_recent_image = image_entry

        if most_recent_image:
            latest_image_per_version[version_label] = most_recent_image

    
    return latest_image_per_version

def build_version_summary_report(latest_image_per_version):
    version_summary_report = []

    for version_label, image_data in latest_image_per_version.items():
        parsed_data_labels = image_data.get("parsed_data", {}).get("labels", [])
        vcs_ref_value = None

        for label_entry in parsed_data_labels:
            if label_entry.get("name") == "vcs-ref":
                vcs_ref_value = label_entry.get("value")
                break

        image_repositories = image_data.get("repositories", [])
        published_date_string = image_repositories[0].get("published_date") if image_repositories else None

        image_freshness_grades = image_data.get("freshness_grades", [])
        freshness_grade_value = image_freshness_grades[0].get("grade") if image_freshness_grades else None

        version_summary_report.append({
            "contentStream": version_label,
            "vcsRef": vcs_ref_value,
            "publishedDate": published_date_string,
            "freshnessGrade": freshness_grade_value,
        })

    return version_summary_report

def main():
    keycloak_images_api_data = fetch_keycloak_images_in_catalog()
    images_grouped_by_version = group_images_by_version_label(keycloak_images_api_data)
    latest_image_per_version = select_latest_image_per_version(images_grouped_by_version)
    print(json.dumps(build_version_summary_report(latest_image_per_version), indent=2))
    return build_version_summary_report(latest_image_per_version)



if __name__ == "__main__":
    main()

