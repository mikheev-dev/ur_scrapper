from multiprocessing import Process, Queue
from typing import List, Tuple, Optional

import asyncio
import aiohttp
import logging
import pydantic
import time

from scrapper.constants import CHUNK_SIZE
from scrapper.finish_object import FINISH_OBJECT
from scrapper.ur_objects_parsers.ur_base_parser import UrBaseParser
from scrapper.ur_models import DependedObjectUrlModel


logger = logging.getLogger(__name__)


class MPUrPuller(Process):
    _src_q: Queue
    _objects_dst_q: Queue
    _depended_objects_urls_q: Optional[Queue]
    _object_parser: UrBaseParser
    _chunk_size: int

    _number_of_extracted_objects: int = 0

    def __init__(
            self,
            object_parser: UrBaseParser,
            src_q: Queue,
            objects_dst_q: Queue,
            depended_objects_urls_q: Optional[Queue],
            chunk_size: int = CHUNK_SIZE,
    ):
        super().__init__()
        self._src_q = src_q
        self._objects_dst_q = objects_dst_q
        self._depended_objects_urls_q = depended_objects_urls_q
        self._object_parser = object_parser
        self._chunk_size = chunk_size

    @staticmethod
    def _handle_exceptions(
            data_chunk: List[DependedObjectUrlModel],
            gathered_data: Tuple[Tuple[List[pydantic.BaseModel], List[DependedObjectUrlModel]]]
    ) -> List[Tuple[List[pydantic.BaseModel], List[DependedObjectUrlModel]]]:
        cleared_gathered_data = []
        for url_model, data in zip(data_chunk, gathered_data):
            if isinstance(data, Exception):
                logger.exception(f"Exception {data} occurred while parsing objects from url {url_model.url}; "
                                 f"Skipped data for it")
            else:
                cleared_gathered_data.append(data)
        return cleared_gathered_data

    @staticmethod
    def _squeeze_gathered_data(
            gathered_data: List[Tuple[List[pydantic.BaseModel], List[DependedObjectUrlModel]]]
    ) -> Tuple[List[pydantic.BaseModel], List[DependedObjectUrlModel]]:
        st_time = time.time()

        all_objects = []
        all_depended_objects_urls = []
        for objects, depended_objects_urls in gathered_data:
            all_objects.extend(objects)
            all_depended_objects_urls.extend(depended_objects_urls)

        logger.debug(f"Squeeze to {len(all_objects)} for {time.time() - st_time}")
        return all_objects, all_depended_objects_urls

    async def _gather_data(
            self,
            data_chunk: List[DependedObjectUrlModel],
            session: aiohttp.ClientSession
    ) -> Tuple[Tuple[List[pydantic.BaseModel], List[DependedObjectUrlModel]]]:
        gathered_data = await asyncio.gather(*[
            self._object_parser.get_scrapped_objects(
                depended_object=url_object,
                session=session,
            )
            for url_object in data_chunk
        ], return_exceptions=True)
        return gathered_data

    async def _handle_chunk_data(self, data_chunk: List[DependedObjectUrlModel], session: aiohttp.ClientSession):
        st_time = time.time()

        gathered_data = await self._gather_data(
            data_chunk=data_chunk,
            session=session,
        )

        gathered_data = self._handle_exceptions(data_chunk, gathered_data)
        objects, depended_objects_urls = self._squeeze_gathered_data(gathered_data)

        for obj in objects:
            self._objects_dst_q.put(obj)
        if self._depended_objects_urls_q:
            for depended_object_url in depended_objects_urls:
                self._depended_objects_urls_q.put(depended_object_url)

        self._number_of_extracted_objects += len(objects)
        logger.info(f"Extracted {len(objects)} objects of type {self._object_parser.PARSED_OBJECT_TYPE_NAME} "
                    f"for {time.time() - st_time}s")

    async def _async_run(self):
        async with aiohttp.ClientSession() as session:
            objects_chunk = []
            while True:
                obj_from_src_q = self._src_q.get()
                if obj_from_src_q == FINISH_OBJECT:
                    break
                objects_chunk.append(obj_from_src_q)
                if len(objects_chunk) == self._chunk_size:
                    await self._handle_chunk_data(objects_chunk, session)
                    objects_chunk = []

            if objects_chunk:
                await self._handle_chunk_data(objects_chunk, session)

            self._objects_dst_q.put(FINISH_OBJECT)

            if self._depended_objects_urls_q:
                self._depended_objects_urls_q.put(FINISH_OBJECT)

    def run(self):
        st_time = time.time()
        asyncio.run(self._async_run())
        logger.info(f"Total extracted {self._number_of_extracted_objects} "
                    f"of type {self._object_parser.PARSED_OBJECT_TYPE_NAME} for {time.time() - st_time}s")

