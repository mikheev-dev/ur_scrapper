from multiprocessing import Process, Queue
from typing import List

import logging
import os
import time

from scrapper.constants import UR_URL, CATALOGUE_POSTFIX
from scrapper.finish_object import FINISH_OBJECT
from scrapper.ur_objects_pullers.mp_ur_puller import MPUrPuller
from scrapper.ur_objects_parsers import (
    UrManufacturersParser,
    UrCategoriesParser,
    UrModelsParser,
    UrPartsParser,
)
from scrapper.ur_objects_serializers import PydanticToCSVSerializer
from scrapper.ur_objects_savers import (
    FileSaver,
    MPFileSaver,
)
from scrapper.ur_models import DependedObjectUrlModel

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UrScrapper:
    _savers_processes: List[Process]
    _pullers_processes: List[Process]

    def __init__(
            self,
            manufacturers_file_path: str,
            categories_file_path: str,
            models_file_path: str,
            parts_file_path: str,
    ):
        self._savers_processes = []
        self._pullers_processes = []

        # Init queues for savers
        self._manufacturers_saver_q = Queue()
        self._categories_saver_q = Queue()
        self._models_saver_q = Queue()
        self._parts_saver_q = Queue()

        # Init manufacturer saver
        self._manufacturer_serializer = PydanticToCSVSerializer(
            fields_order=["name"]
        )
        self._manufacturer_saver = FileSaver(
            path_to_file=manufacturers_file_path,
        )
        self._manufacturers_saver_process = MPFileSaver(
            q=self._manufacturers_saver_q,
            file_saver=self._manufacturer_saver,
            serializer=self._manufacturer_serializer
        )
        self._savers_processes.append(self._manufacturers_saver_process)

        # Init categories saver
        self._category_serializer = PydanticToCSVSerializer(
            fields_order=["name"]
        )
        self._categories_saver = FileSaver(
            path_to_file=categories_file_path,
        )
        self._categories_saver_process = MPFileSaver(
            q=self._categories_saver_q,
            file_saver=self._categories_saver,
            serializer=self._category_serializer
        )
        self._savers_processes.append(self._categories_saver_process)

        # Init models saver
        self._models_serializer = PydanticToCSVSerializer(
            fields_order=["name", "manufacturer_name"]
        )
        self._models_saver = FileSaver(
            path_to_file=models_file_path,
        )
        self._models_saver_process = MPFileSaver(
            q=self._models_saver_q,
            file_saver=self._models_saver,
            serializer=self._models_serializer
        )
        self._savers_processes.append(self._models_saver_process)

        # Init parts saver
        self._parts_serializer = PydanticToCSVSerializer(
            fields_order=["number", "spec", "name_of_model", "category_name"]
        )
        self._parts_saver = FileSaver(
            path_to_file=parts_file_path,
        )
        self._parts_saver_process = MPFileSaver(
            q=self._parts_saver_q,
            file_saver=self._parts_saver,
            serializer=self._parts_serializer
        )
        self._savers_processes.append(self._parts_saver_process)

        # Init queues for sending url object
        self._manufacturers_urls_q = Queue()
        self._categories_urls_q = Queue()
        self._models_urls_q = Queue()
        self._parts_urls_q = Queue()

        # Init parsers
        self._manufacturers_parser = UrManufacturersParser()
        self._categories_parser = UrCategoriesParser()
        self._models_parser = UrModelsParser()
        self._parts_parser = UrPartsParser()

        # Init process for extracting Manufacturers from urls
        self._manufacturer_puller_process = MPUrPuller(
            object_parser=self._manufacturers_parser,
            src_q=self._manufacturers_urls_q,
            objects_dst_q=self._manufacturers_saver_q,
            depended_objects_urls_q=self._categories_urls_q,
        )
        self._pullers_processes.append(self._manufacturer_puller_process)

        # Init process for extracting categories from urls
        self._categories_puller_process = MPUrPuller(
            object_parser=self._categories_parser,
            src_q=self._categories_urls_q,
            objects_dst_q=self._categories_saver_q,
            depended_objects_urls_q=self._models_urls_q,
        )
        self._pullers_processes.append(self._categories_puller_process)

        # Init process for extracting models from urls
        self._models_puller_process = MPUrPuller(
            object_parser=self._models_parser,
            src_q=self._models_urls_q,
            objects_dst_q=self._models_saver_q,
            depended_objects_urls_q=self._parts_urls_q,
        )
        self._pullers_processes.append(self._models_puller_process)

        # Init process for extracting parts from urls
        self._parts_puller_process = MPUrPuller(
            object_parser=self._parts_parser,
            src_q=self._parts_urls_q,
            objects_dst_q=self._parts_saver_q,
            depended_objects_urls_q=None,
            chunk_size=10,
        )
        self._pullers_processes.append(self._parts_puller_process)

    def scrap(self):
        st_time = time.time()
        logger.info("Start scrapping UR")

        for saver_proc in self._savers_processes:
            saver_proc.start()

        for puller_proc in self._pullers_processes:
            puller_proc.start()

        self._manufacturers_urls_q.put(
            DependedObjectUrlModel(
                url=os.path.join(UR_URL, CATALOGUE_POSTFIX),
                meta=dict(),
            )
        )

        self._manufacturers_urls_q.put(
            FINISH_OBJECT
        )

        for puller_proc in self._pullers_processes:
            puller_proc.join()

        for saver_proc in self._savers_processes:
            saver_proc.join()

        logger.info(f"Scrapped UR for {time.time() - st_time}")

# chunk_size=30 ; time=383s
# chunk_size=1 ; time>10min
# chunk_size=10; time=353s
# chunk_size=5; time=375s
# chunk_size=20; time=362s
