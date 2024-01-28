from typing import List

import logging
import os

from constants import UR_URL
from ur_models import URManufacturer, DependedObjectUrlModel
from ur_objects_parsers.ur_base_parser import UrBaseParser

logger = logging.getLogger(__name__)


class UrManufacturersParser(UrBaseParser):
    _CONTAINER_CLASS_NAME: str = "c_container allmakes"
    PARSED_OBJECT_TYPE_NAME: str = "MANUFACTURER"

    @staticmethod
    def _get_objects(
            items: List,
            depended_object: DependedObjectUrlModel,
    ) -> List[URManufacturer]:
        return [
            URManufacturer(
                name=manufacturer_item.text.strip(),
            )
            for manufacturer_item in items
        ]

    @staticmethod
    def _get_depended_urls_objects(
            items: List,
            depended_object: DependedObjectUrlModel
    ) -> List[DependedObjectUrlModel]:
        return [
            DependedObjectUrlModel(
                url=os.path.join(UR_URL, manufacturer_item.get("href")),
                meta={
                    "manufacturer_name": manufacturer_item.text.strip(),
                }
            )
            for manufacturer_item in items
        ]


