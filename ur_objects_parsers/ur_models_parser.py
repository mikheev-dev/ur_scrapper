from typing import List

import logging
import os

from constants import UR_URL
from ur_models import URModel, DependedObjectUrlModel
from ur_objects_parsers.ur_base_parser import UrBaseParser


logger = logging.getLogger(__name__)


class UrModelsParser(UrBaseParser):
    _CONTAINER_CLASS_NAME: str = "c_container allmodels"
    PARSED_OBJECT_TYPE_NAME: str = "MODEL"

    @staticmethod
    def _get_objects(
            items: List,
            depended_object: DependedObjectUrlModel,
    ) -> List[URModel]:
        return [
            URModel(
                name=model_item.text.strip(),
                manufacturer_name=depended_object.meta.get("manufacturer_name"),
            )
            for model_item in items
        ]

    @staticmethod
    def _get_depended_urls_objects(
            items: List,
            depended_object: DependedObjectUrlModel
    ) -> List[DependedObjectUrlModel]:
        return [
            DependedObjectUrlModel(
                url=os.path.join(UR_URL, model_item.get("href")),
                meta={
                    "model_name": model_item.text.strip(),
                    "category_name": depended_object.meta.get("category_name")
                }
            )
            for model_item in items
        ]


