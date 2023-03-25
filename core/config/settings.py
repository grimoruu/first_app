import os

import yaml

from core.config.schema import Settings


def get_settings(p: str) -> Settings:
    with open(os.path.abspath(p)) as f:
        return Settings.parse_obj(yaml.safe_load(f))


settings = get_settings("/home/grimoruu/PycharmProjects/first_app/config.yml")
