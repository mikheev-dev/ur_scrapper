from typing import List

import logging
import os

from scrapper.constants import UR_URL
from scrapper.ur_models import URCategory, DependedObjectUrlModel
from scrapper.ur_objects_parsers.ur_base_parser import UrBaseParser


logger = logging.getLogger(__name__)


class UrCategoriesParser(UrBaseParser):
    """
    Class to extract Category objects from URParts site
    """
    _CONTAINER_CLASS_NAME: str = "c_container allmakes allcategories"
    PARSED_OBJECT_TYPE_NAME: str = "CATEGORY"

    @staticmethod
    def _get_objects(
            items: List,
            depended_object: DependedObjectUrlModel,
    ) -> List[URCategory]:
        return [
            URCategory(
                name=category_item.text.strip(),
            )
            for category_item in items
        ]

    @staticmethod
    def _get_depended_urls_objects(
            items: List,
            depended_object: DependedObjectUrlModel
    ) -> List[DependedObjectUrlModel]:
        return [
            DependedObjectUrlModel(
                url=os.path.join(UR_URL, category_item.get("href")),
                meta={
                    "manufacturer_name": depended_object.meta.get("manufacturer_name"),
                    "category_name": category_item.text.strip(),
                }
            )
            for category_item in items
        ]


