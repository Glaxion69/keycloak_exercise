# Keyclock Assesment

Pre req:
1. python version: 3.11
2. pip 25.2
3. [Dev Deps] Black Linter

## Install dependency:
```
pip install -r requires.txt
```

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
Filter the returned object from previous function as per Content streams labels and use use the same to return a sorted dict with k: label version and v: all its images metadata

### Step 3:
Next select the Most Recent Image per Content Stream (k), get a function function to sort and return k: label (example: 26.2) and v: latest image metadata

### Step 4
Get all the relevent fields from prev result and return/display them



## Limitation/Future Scope:
- Use conda / Poetry
- Create a CLI for custom input adoption
