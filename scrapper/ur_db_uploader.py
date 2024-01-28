from sqlalchemy import create_engine
from typing import List, Dict
from yoyo import read_migrations, get_backend

import logging
import pandas as pd
import time

from config import PSQLConfig

logger = logging.getLogger(__name__)


class UrDbUploader:
    """
    Class to upload scrapped data from files to database and normalize data
    """
    _path_to_initial_migrations_dir: str
    _path_to_normalization_migrations_dir: str

    _tables_source_files_paths: Dict[str, str]

    def __init__(
            self,
            initial_migrations_dir: str,
            normalization_migrations_dir: str,
    ):
        self._path_to_initial_migrations_dir = initial_migrations_dir
        self._path_to_normalization_migrations_dir = normalization_migrations_dir

    @staticmethod
    def _apply_migrations(migrations_dir: str):
        backend = get_backend(PSQLConfig.connection_string())
        migrations = read_migrations(migrations_dir)

        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))

    def apply_initial_migrations(self):
        """
        Apply initial migrations to create initial tables for scrapped data
        """

        logger.info("Applying initial migrations.")
        st_time = time.time()
        self._apply_migrations(self._path_to_initial_migrations_dir)
        logger.info(f"Applied initial migrations for {time.time() - st_time}s")

    def apply_normalizing_ur_data_migrations(self):
        """
        Apply migrations to normalize uploaded data
        """
        logger.info("Applying normalizing migrations.")
        st_time = time.time()
        self._apply_migrations(self._path_to_normalization_migrations_dir)
        logger.info(f"Applied normalizing migrations for {time.time() - st_time}s")

    def upload_csv_data(
            self,
            table_name: str,
            table_fields: List[str],
            path_to_csv_file: str,
    ):
        """
        Upload data from csv file to table.

        :param table_name: table name to upload data to
        :param table_fields: list of table columns names in which data is stored in csv
        :param path_to_csv_file: path to csv file
        :return:
        """
        logger.info(f"Started uploading {path_to_csv_file} to table {table_name}.")
        st_time = time.time()
        df = pd.read_csv(
            path_to_csv_file,
            names=table_fields,
            delimiter='\t',
        )
        engine = create_engine(PSQLConfig.connection_string())
        df.to_sql(table_name, engine, if_exists='append', index=False, )
        logger.debug(f"Upload file {path_to_csv_file} to table {table_name} for {time.time() - st_time}s")

