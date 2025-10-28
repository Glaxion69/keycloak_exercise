# Keyclock Assesment

Generates JSON reports on the most recent `rhbk/keycloak-rhel9` container images per content stream from the Red Hat Ecosystem Catalog.


## Quickstart

Run the following bash script for end-to-end execution. this is the simplest way to run generate_keycloak_stream_report.py

Make the script as an executable
```bash
chmod +x run.sh
```
Run the script
```bash
./run.sh
```
## Developer mode

Prerequisites:
1. python version: 3.11
2. pip 25.2
3. [Dev Deps] Black Linter

## Install dependency:
```
pip install -r requires.txt
```
## Optional .env support

### `REDHAT_CATALOG_BASE_URL`
Description:Base URL for the Red Hat Container Catalog API. Defaults to `https://catalog.redhat.com/api/containers/v1` if not set.

Example value:`https://catalog.redhat.com/api/containers/v1`

### `LOG_LEVEL`
Description: Controls logging verbosity. Supported values: `DEBUG`, `INFO`, `WARNING`, `ERROR`. Defaults to `INFO`.

Example value: `DEBUG`

## Usage
```
python generate_keycloak_stream_report.py
```

### To save the Output in a JSON file
```
python generate_keycloak_stream_report.py > report.json
```

## Intuition

### Step 1
Hit the endpoint: https://catalog.redhat.com/api/containers/v1/repositories/registry/registry.access.redhat.com/repository/rhbk%2Fkeycloak-rhel9/images
and get a json with list of all the image metadata and data in the specified Repository (rhbk/keycloak-rhel9)

### Step 2
Filter the returned object from previous function as per Content streams labels and use the same to return a sorted dict with k: label version and v: all its images metadata

### Step 3:
Next select the Most Recent Image per Content Stream (k), get a function to sort and return k: label (example: 26.2) and v: latest image metadata

### Step 4
Get all the relevant fields from previous result and return/display them.



## Limitation/Future Scope:
- Use conda / Poetry
- Create a CLI for custom input adoption
