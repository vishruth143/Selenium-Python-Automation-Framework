# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long, too-few-public-methods

import os
from pta_automation.framework.utilities.loaders import load_json, load_yaml

class ConfigParser:
    CONFIG_FILE_PATHS = {
        'common_config': 'common_config.yaml',
        'ui_test_env_config': 'ui/ui_test_env_config.yaml',
        'ui_test_data_config': 'ui/ui_test_data_config.yaml',
        'api_test_env_config': 'api/api_test_env_config.yaml',
        'api_test_data_config': 'api/api_test_data_config.json',
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