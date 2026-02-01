from functools import lru_cache
from typing import Dict, Type

from item.src.core.settings.app import AppSettings
from item.src.core.settings.base import AppEnvTypes, BaseAppSettings
from item.src.core.settings.development import DevAppSettings
from item.src.core.settings.production import ProdAppSettings
from item.src.core.settings.test import TestAppSettings

environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
