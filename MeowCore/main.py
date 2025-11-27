# iSHiKKi-Akabane - LilianPark

import requests
import logging
import aiohttp
import asyncio
import zipfile
import io


class MeowLogger:
    def __init__(self):
        self.logger = logging.getLogger("MeowCore")

    def info(self, message: str):
        self.logger.info(f"[MEOWCORE] INFO » {message}")

    def warning(self, message: str):
        self.logger.warning(f"[MEOWCORE] WARNING » {message}")

    def error(self, message: str):
        self.logger.error(f"[MEOWCORE] ERROR » {message}")

    def debug(self, message: str):
        self.logger.debug(f"[MEOWCORE] DEBUG » {message}")


logger = MeowLogger()


class MeowCore:
    """
    MeowCore 🐾 - A cat-tastic Python library that offers versatile utilities for developers.
    
    Attributes:
    -----------
    api_key : str
        Stores a general API key (None by default).
    bot_name : str
        Stores the AI service key (None by default).
    """


    def __init__(
        self,
        api_key: str,
        bot_name: str
    ):
        """
        Initialize MeowCore with the given API token. Automatically triggers 
        authentication with the MeowCore API to validate the provided token.

        :param api_key: The api token for the running MeowCore.
        :param bot_name: A human-readable identifier for the bot.
        :raises ValueError: If authentication fails due to invalid token.
        """
        self.api_key = api_key
        self.bot_name = bot_name
        self.meow_api = "https://meow-core-api.vercel.app"
        self.category = "telegram"
        self.authenticate()


    def authenticate(self):
        """
        Authenticate the user with the MeowCore API using the provided token.

        :raises ValueError: If the token is invalid or authentication fails.
        """
        logger.info("Initialising MeowCore Instance...")
        
        if self.category not in ["telegram"]:
            logger.error("Invalid category provided for MeowCore. Access Denied!")
            raise ValueError("Invalid category provided for MeowCore.")
            
        if not self._validate_token():
            logger.error("Invalid API key provided for MeowCore. Access Denied!")
            raise ValueError("Invalid API key provided for MeowCore.")
        logger.info("MeowCore loaded successfully!!! Ready to purr and serve.")


    def _validate_token(self):
        """
        Sends a POST request to the MeowCore API to validate the provided token.

        If authentication is successful, the response contains various keys like
        AI key, scanner key, and a general API key, which are stored for future use.

        :return: True if the token is valid and authentication is successful, False otherwise.
        :raises ConnectionError: If there is an issue connecting to the MeowCore API.
        :raises requests.RequestException: If an error occurs during the POST request.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(
                f"{self.meow_api}/auth", headers=headers
            )
            if response.status_code == 200:
                logger.info("Token validated successfully. You have purr-mission!")
                response_data = response.json()
                self.user = response_data["user"]
                self.plugins = response_data["plugins"]
                return True
            else:
                logger.warning(f"Token validation failed! Status code: {response.status_code}.")
                return False
        except requests.RequestException as e:
            logger.error(f"An error occurred during token validation: {e}. Looks like something went wrong!")
            raise ConnectionError("Error connecting to MeowCore...")
        except Exception as e:
            logger.error(f"An error occurred during token validation: {e}. Looks like something went wrong!")
            return False
    
    def load_plugins(self, download_dir="./"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        try:
            logger.info("Downloading Plugins...!")
            payload = {"plugin-codes": self.plugins}
            response = requests.post(
                f"{self.meow_api}/downloadall",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                zip_filename = "plugins.zip"
                file_downloaded = []
                with open(zip_filename, 'wb') as f:
                    f.write(response.content)
                try:
                    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                        z.extractall(download_dir)
                        logger.info(f"Extracted: {z.namelist()} into {download_dir}")
                except zipfile.BadZipFile:
                    logger.error("Error: The file downloaded was not a valid zip file.")
            else:
                logger.warning(f"Download failed! : {response.json()}.")
                return False
        except requests.RequestException as e:
            logger.error(f"An error occurred during downloading: {e}. Looks like something went wrong!")
            raise ConnectionError("Error Downloading to MeowCore...")
        except Exception as e:
            logger.error(f"An error occurred during downloading plugins: {e}. Looks like something went wrong!")
            return False



