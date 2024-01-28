import os
import tarfile

from scrapper.constants import PATH_TO_SCRAPPED_DATA, PARTS_TGZ_NAME


class FilesExtractor:
    @staticmethod
    def extract_parts():
        part_file = tarfile.open(os.path.join(PATH_TO_SCRAPPED_DATA, PARTS_TGZ_NAME))
        part_file.extractall(PATH_TO_SCRAPPED_DATA)
        part_file.close()
