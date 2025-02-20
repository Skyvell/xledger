import os
import logging

class EnvironmentConfig:
    """
    A class to encapsulate the environment configuration for the application.

    This class fetches and validates required environment variables used 
    throughout the application. It raises a ValueError if any of the required 
    environment variables are missing.
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
        self.employee_groups_flex_link = self.get_env_variable("EMPLOYEE_GROUPS_FLEX_LINK")
        self.emploment_types_flex_link = self.get_env_variable("EMPLOYMENT_TYPES_FLEX_LINK")
        self.project_groups_flex_link = self.get_env_variable("PROJECT_GROUPS_FLEX_LINK")
        self.financial_results_flex_link = self.get_env_variable("FINANCIAL_RESULTS_FLEX_LINK")
        self.part_time_data_ductus_ab_flex_link = self.get_env_variable("PART_TIME_DATA_DUCTUS_AB_FLEX_LINK")
        self.part_time_data_ductus_holding_ab_flex_link = self.get_env_variable("PART_TIME_DATA_DUCTUS_HOLDING_AB_FLEX_LINK")
        self.part_time_data_ductus_luleå_ab_flex_link = self.get_env_variable("PART_TIME_DATA_DUCTUS_LULEÅ_AB_FLEX_LINK")
        # self.part_time_data_ductus_inc_flex_link = self.get_env_variable("PART_TIME_DATA_DUCTUS_INC_FLEX_LINK")
        # self.part_time_tromb_ab_flex_link = self.get_env_variable("PART_TIME_TROMB_AB_FLEX_LINK")

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