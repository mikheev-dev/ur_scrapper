from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import List, Tuple

import aiohttp
import logging
import pydantic
import time

from scrapper.ur_models import DependedObjectUrlModel

logger = logging.getLogger(__name__)


class UrBaseParser(ABC):
    """
    Class for extracting objects from URPart urls
    """
    _CONTAINER_CLASS_NAME: str
    PARSED_OBJECT_TYPE_NAME: str

    @staticmethod
    async def _get_parsed_html_page(url: str, session: aiohttp.ClientSession) -> BeautifulSoup:
        """
        Get HTML page which contains objects.
        :param url: url to get
        :param session: aiohttp session
        :return: parsed HTML page
        """
        async with session.get(url) as resp:
            raw_page = await resp.text()
        return BeautifulSoup(raw_page, "html.parser")

    @staticmethod
    def _get_items_from_named_container(
            page: BeautifulSoup,
            container_class_name: str,
    ) -> List:
        """
        Find HTML containers with objects to parse
        :param page: HTML page
        :param container_class_name: target container name
        :return: list of HTML container to get objects from
        """
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
        """
        Method to extract objects from HTML containers.
        :param items: HTML containers
        :param depended_object: Object with meta information from higher-level object
        from which the url for current objects was got
        :return: list of objects
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _get_depended_urls_objects(
            items: List,
            depended_object: DependedObjectUrlModel
    ) -> List[DependedObjectUrlModel]:
        """
        Method to extract information from HTML containers of deeper objects: url and meta
        :param items: HTML containers
        :param depended_object: Object with meta information from higher-level object for creating new meta
        :return: list of objects contained urls and meta for getting object
        """
        raise NotImplementedError

    @classmethod
    async def get_scrapped_objects(
            cls,
            depended_object: DependedObjectUrlModel,
            session: aiohttp.ClientSession,
    ) -> Tuple[List[pydantic.BaseModel], List[DependedObjectUrlModel]]:
        """
        Method to extract objects using url from depended_object
        :param depended_object: object with url and meta information
        :param session: aiohttp session
        :return: tuple of extracted objects and objects to extract deeper objects
        """
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

