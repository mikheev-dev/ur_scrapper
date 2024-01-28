from typing import Callable, Any

import os


def get_env(name: str, default: Any = None, cast: Callable[[Any], Any] = lambda x: x):
    value = os.getenv(name) or default
    return cast(value)


class PSQLConfig:
    DB_HOST = get_env('DB_HOST', default='0.0.0.0')
    DB_PORT = get_env('DB_PORT', default='5432', cast=int)
    DB_USER = get_env('DB_USER', default='uradmin')
    DB_PASSWORD = get_env('DB_PASS', default='test77')
    DB_NAME = get_env('DB_NAME', default='urdb')

    @staticmethod
    def connection_string() -> str:
        return (f"postgresql://{PSQLConfig.DB_USER}:{PSQLConfig.DB_PASSWORD}@"
                f"{PSQLConfig.DB_HOST}:{PSQLConfig.DB_PORT}/{PSQLConfig.DB_NAME}")


class ScrapperAppConfig:
    PATH_TO_SCRAPPED_FILES_DIR = "scrapped_data"

    MANUFACTURERS_FILE_NAME = "manufacturer.csv"
    CATEGORIES_FILE_NAME = "categories.csv"
    MODELS_FILE_NAME = "models.csv"
    PARTS_FILE_NAME = "parts.csv"

    MANUFACTURERS_FILE_PATH = os.path.join(PATH_TO_SCRAPPED_FILES_DIR, MANUFACTURERS_FILE_NAME)
    CATEGORIES_FILE_PATH = os.path.join(PATH_TO_SCRAPPED_FILES_DIR, CATEGORIES_FILE_NAME)
    MODELS_FILE_PATH = os.path.join(PATH_TO_SCRAPPED_FILES_DIR, MODELS_FILE_NAME)
    PARTS_FILE_PATH = os.path.join(PATH_TO_SCRAPPED_FILES_DIR, PARTS_FILE_NAME)

    INITIAL_MIGRATIONS_DIR = "migrations/initial_migrations"
    NORMALIZATION_MIGRATIONS_DIR = "migrations/normalizing_ur_data_migrations"

    MANUFACTURERS_TABLE_NAME = "manufacturers"
    MANUFACTURERS_TABLE_FIELDS = ["name"]

    CATEGORIES_TABLE_NAME = "categories"
    CATEGORIES_TABLE_FIELDS = ["name"]

    MODELS_TABLE_NAME = "models"
    MODELS_TABLE_FIELDS = ["name", "manufacturer_name"]

    PARTS_TABLE_NAME = "parts_models_categories"
    PARTS_TABLE_FIELDS = ["number", "spec", "model_name", "category_name"]

    UPLOAD_DATA_WITHOUT_SCRAPPING: bool = get_env("UPLOAD_DATA_WITHOUT_SCRAPPING", default=False, cast=bool)
