class ApiRespondedNullException(Exception):
    def __init__(self, endpoint_url):
        super().__init__(f"API at '{endpoint_url}' responded with null or empty data.")


class ApiResponseUnexpectedFormatException(Exception):
    def __init__(self, endpoint_url):
        super().__init__(
            f"API response from '{endpoint_url}' is in an unexpected format."
        )


class UnexpectedSteamVersionException(Exception):
    def __init__(self, endpoint_data):
        super().__init__(
            f"Failed to fetch relevant label version value from '{endpoint_data}'"
        )


class InvalidImageDataFoundException(Exception):
    def __init__(self, context=""):
        super().__init__(f"No valid images found with proper information :-'{context}'")


class UnexpectedDateFormat(Exception):
    def __init__(self, date_string):
        super().__init__(f"Unsupported Date format '{date_string}'")
