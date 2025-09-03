# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long, too-few-public-methods

import os

import pandas as pd

from framework.utilities.loaders import load_json, load_yaml, load_xlsx_sheet

class ConfigParser:
    CONFIG_FILE_PATHS = {
        'common_config': 'common_config.yml',
        'pta_ui_test_env_config': 'ui/pta/ui_test_env_config.yml',
        'pta_ui_test_data_config': 'ui/pta/ui_test_data_config.yml',
        'pta_ui_test_excel_data_config': 'ui/pta/ui_test_excel_data_config.xlsx',
        'reqres_api_test_env_config': 'api/reqres/api_test_env_config.yml',
        'reqres_api_test_data_config': 'api/reqres/api_test_data_config.json',
        'darden_commerce_tools_api_test_env_config': 'api/darden_commerce_tools/api_test_env_config.yml',
        'darden_commerce_tools_api_test_data_config': 'api/darden_commerce_tools/api_test_data_config.json',
    }

    @staticmethod
    def load_config(config_name):
        config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), ConfigParser.CONFIG_FILE_PATHS[config_name]))
        _, ext = os.path.splitext(config_path)
        if ext == '.json':
            config = load_json(config_path)
        elif ext in ('.yaml', '.yml'):
            config = load_yaml(config_path)
        else:
            raise ValueError(f'Unsupported file extension: {ext}')
        return config

    @staticmethod
    def load_xlsx(config_name: str, sheet_name: str) -> pd.DataFrame:
        """
        Load a specified sheet from an Excel file.

        :param sheet_name: Name of the sheet to load.
        :return: pandas DataFrame containing the sheet data.
        """
        config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), ConfigParser.CONFIG_FILE_PATHS[config_name]))
        _, ext = os.path.splitext(config_path)

        if ext == '.xlsx':
            df = load_xlsx_sheet(config_path, sheet_name)
        else:
            raise ValueError(f'Unsupported file extension: {ext}')

        return df

    @staticmethod
    def resolve_config_path(config_name: str) -> str:
        """
        Resolve absolute path of the given config file name.
        :param config_name: Key from CONFIG_FILE_PATHS
        :return: Absolute path to the config file
        """
        return os.path.abspath(
            os.path.join(os.path.dirname(__file__), ConfigParser.CONFIG_FILE_PATHS[config_name])
        )