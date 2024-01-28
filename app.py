import logging
import os

from ur_scrapper import UrScrapper
from ur_db_uploader import UrDbUploader
from config import ScrapperAppConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    if ScrapperAppConfig.SCRAP_DATA:
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

    if ScrapperAppConfig.UPLOAD_DATA:
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
