
import requests
import logging

logger = logging.getLogger('MeowCore')
logger.setLevel(logging.DEBUG)


class MeowCore:
    """
    MeowCore 🐾 - A cat-tastic Python library that offers versatile utilities for developers.
    
    Attributes:
    -----------
    token : str
        The secret key (API token) to authenticate users.
    ai_key : str
        Stores the AI service key (None by default).
    scanner_key : str
        Stores the scanner service key (None by default).
    api_key : str
        Stores a general API key (None by default).
    meow_api : str
        The base URL for MeowCore API authentication.
    """

    def __init__(self, TOKEN: str):
        """
        Initializes MeowCore with the given API token. 
        Automatically calls the authenticate method to validate the token.
        
        Parameters:
        -----------
        TOKEN : str
            The API token that purr-mits access to MeowCore services.
        """
        self.token = TOKEN
        self.ai_key = None
        self.scanner_key = None
        self.api_key = None
        self.apiurl = None
        self.meow_api = "https://meow.api"
        self.authenticate()

    def authenticate(self):
        """
        Authenticates the user with the provided API token.
        If the token is invalid, the library raises a ValueError and logs an error.
        """
        if not self._validate_token():
            logger.error("Invalid API key provided for MeowCore 🐾. Access Denied! 😿")
            raise ValueError("Invalid API key provided for MeowCore.")
        
        logger.info("MeowCore loaded successfully!!! 🐾 Ready to purr and serve. 😸")

    def _validate_token(self):
        """
        Sends a POST request to the MeowCore API to validate the API token.
        
        Returns:
        --------
        bool
            True if the token is valid, False otherwise.
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(
                f"{self.meow_api}/auth", headers=headers
            )
            if response.status_code == 200:
                logger.info("Token validated successfully. You have purr-mission! 😺")
                key_data = response.json()["apikey"]
                self.ai_key = key_data["ai_key"]
                self.scanner_key = key_data["scanner_key"]
                self.api_key = key_data["api_key"]
                self.apiurl = response.json()["api_url"]
                return True
            else:
                logger.warning(f"Token validation failed! Status code: {response.status_code}. 😿")
                return False
        except Exception as e:
            logger.error(f"An error occurred during token validation: {e}. Looks like something went wrong! 😿")
            return False

