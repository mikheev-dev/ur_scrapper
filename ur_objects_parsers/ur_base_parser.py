from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import List, Tuple

import aiohttp
import logging
import pydantic
import time

from ur_models import DependedObjectUrlModel

logger = logging.getLogger(__name__)


class UrBaseParser(ABC):
    _CONTAINER_CLASS_NAME: str
    PARSED_OBJECT_TYPE_NAME: str

    @staticmethod
    async def _get_parsed_html_page(url: str, session: aiohttp.ClientSession) -> BeautifulSoup:
        async with session.get(url) as resp:
            raw_page = await resp.text()
        return BeautifulSoup(raw_page, "html.parser")

    @staticmethod
    def _get_items_from_named_container(
            page: BeautifulSoup,
            container_class_name: str,
    ) -> List:
        target_div = page.find("div", class_=container_class_name)
        if not target_div:
            return []
        return target_div.find_all("a")

    @staticmethod
    @abstractmethod
    def _get_objects(
            items: List,
            depended_object: DependedObjectUrlModel
    ) -> List[pydantic.BaseModel]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _get_depended_urls_objects(
            items: List,
            depended_object: DependedObjectUrlModel
    ) -> List[DependedObjectUrlModel]:
        raise NotImplementedError

    @classmethod
    async def get_scrapped_objects(
            cls,
            depended_object: DependedObjectUrlModel,
            session: aiohttp.ClientSession,
    ) -> Tuple[List[pydantic.BaseModel], List[DependedObjectUrlModel]]:
        st_time = time.time()
        page = await cls._get_parsed_html_page(
            url=depended_object.url,
            session=session,
        )
        getting_page_time = time.time() - st_time

        items = cls._get_items_from_named_container(
            page=page,
            container_class_name=cls._CONTAINER_CLASS_NAME,
        )

        objects = cls._get_objects(items, depended_object)
        depended_objects_urls = cls._get_depended_urls_objects(items, depended_object)

        logger.debug(f"Got page for url {depended_object.url} with {len(objects)} objects for {getting_page_time}")

        return objects, depended_objects_urls

