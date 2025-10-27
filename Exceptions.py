class ApiRespondedNullException(Exception):
    def __init__(self, endpoint_url):
        super().__init__(f"API at '{endpoint_url}' responded with null or empty data.")


class ApiResponseUnexpectedFormatException(Exception):
    def __init__(self, endpoint_url):
        super().__init__(f"API response from '{endpoint_url}' is in an unexpected format.")