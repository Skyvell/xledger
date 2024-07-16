import os
import logging

class EnvironmentConfig:
    """
    A class to encapsulate the environment configuration for the application.

    This class fetches and validates required environment variables used 
    throughout the application. It raises a ValueError if any of the required 
    environment variables are missing.

    Attributes:
        api_endpoint (str): The API endpoint for the GraphQL client.
        api_key (str): The API key for the GraphQL client.
        data_storage_account (str): The name of the data storage account.
        data_storage_container (str): The name of the data storage container.
        app_config_endpoint (str): The endpoint for the app configuration.
    """
    
    def __init__(self):
        """
        Initializes the EnvironmentConfig class by fetching and validating
        the required environment variables.
        """
        self.api_endpoint = self.get_env_variable("API_ENDPOINT")
        self.api_key = self.get_env_variable("API_KEY")
        self.data_storage_account = self.get_env_variable("DATA_STORAGE_ACCOUNT_NAME")
        self.data_storage_container = self.get_env_variable("DATA_STORAGE_CONTAINER_NAME")
        self.app_config_endpoint = self.get_env_variable("APP_CONFIG_ENDPOINT")

    @staticmethod
    def get_env_variable(var_name: str) -> str:
        """
        Fetches and validates an environment variable.

        Args:
            var_name (str): The name of the environment variable to fetch.

        Returns:
            str: The value of the environment variable.

        Raises:
            ValueError: If the environment variable is not set.
        """
        value = os.getenv(var_name)
        if not value:
            logging.error(f"Environment variable '{var_name}' is missing.")
            raise ValueError(f"Environment variable '{var_name}' is missing.")
        return value