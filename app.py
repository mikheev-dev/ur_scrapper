import logging
import os

import requests

from scrapper.ur_files_extractor import FilesExtractor
from scrapper.ur_scrapper import UrScrapper
from scrapper.ur_db_uploader import UrDbUploader
from config import ScrapperAppConfig
from scrapper.constants import UR_URL, CATALOGUE_POSTFIX

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    target_url = os.path.join(UR_URL, CATALOGUE_POSTFIX)
    logger.info(f"Check availability of url {target_url}")
    try:
        request_status = requests.get(target_url, timeout=10.0, verify=False).status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Exception {e} occurred while trying to get {target_url}.")
        request_status = 500

    if request_status == 200:
        logger.info("Scrapping UR data")
        os.makedirs(ScrapperAppConfig.PATH_TO_SCRAPPED_FILES_DIR, exist_ok=True)

        scrapper = UrScrapper(
            manufacturers_file_path=ScrapperAppConfig.MANUFACTURERS_FILE_PATH,
            categories_file_path=ScrapperAppConfig.CATEGORIES_FILE_PATH,
            models_file_path=ScrapperAppConfig.MODELS_FILE_PATH,
            parts_file_path=ScrapperAppConfig.PARTS_FILE_PATH,
        )

        scrapper.scrap()
        logger.info("UR data scrapped")
    else:
        logger.info("Scrapping from URL is disabled. Upload data from local dumps.")
        FilesExtractor.extract_parts()

    logger.info("Uploading data to db")
    db_uploader = UrDbUploader(
        initial_migrations_dir=ScrapperAppConfig.INITIAL_MIGRATIONS_DIR,
        normalization_migrations_dir=ScrapperAppConfig.NORMALIZATION_MIGRATIONS_DIR,
    )
    db_uploader.apply_initial_migrations()

    db_uploader.upload_csv_data(
        table_name=ScrapperAppConfig.MANUFACTURERS_TABLE_NAME,
        table_fields=ScrapperAppConfig.MANUFACTURERS_TABLE_FIELDS,
        path_to_csv_file=ScrapperAppConfig.MANUFACTURERS_FILE_PATH,
    )

    db_uploader.upload_csv_data(
        table_name=ScrapperAppConfig.CATEGORIES_TABLE_NAME,
        table_fields=ScrapperAppConfig.CATEGORIES_TABLE_FIELDS,
        path_to_csv_file=ScrapperAppConfig.CATEGORIES_FILE_PATH,
    )

    db_uploader.upload_csv_data(
        table_name=ScrapperAppConfig.MODELS_TABLE_NAME,
        table_fields=ScrapperAppConfig.MODELS_TABLE_FIELDS,
        path_to_csv_file=ScrapperAppConfig.MODELS_FILE_PATH,
    )

    db_uploader.upload_csv_data(
        table_name=ScrapperAppConfig.PARTS_TABLE_NAME,
        table_fields=ScrapperAppConfig.PARTS_TABLE_FIELDS,
        path_to_csv_file=ScrapperAppConfig.PARTS_FILE_PATH,
    )

    db_uploader.apply_normalizing_ur_data_migrations()
    logger.info("Uploaded data to db")
