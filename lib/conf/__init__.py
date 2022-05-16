import importlib
import os

from lib.conf import default_settings

ENVIRONMENT_VARIABLE = "DATACREDITO_SETTINGS_MODULE"


class Settings:
    def __init__(self) -> None:
        default_attributes = dir(default_settings)

        for attribute in default_attributes:
            if attribute.isupper():
                setattr(self, attribute, getattr(default_settings, attribute))

        custom_settings = os.environ.get(ENVIRONMENT_VARIABLE)

        if custom_settings:
            custom_settings_mod = importlib.import_module(custom_settings)
            custom_attributes = dir(custom_settings_mod)

            for attribute in custom_attributes:
                if attribute.isupper():
                    setattr(self, attribute, getattr(custom_settings_mod, attribute))


settings = Settings()
