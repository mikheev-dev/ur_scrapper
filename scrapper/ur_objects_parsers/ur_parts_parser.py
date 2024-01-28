from typing import List

import logging

from scrapper.ur_models import URPart, DependedObjectUrlModel
from scrapper.ur_objects_parsers.ur_base_parser import UrBaseParser


logger = logging.getLogger(__name__)


class UrPartsParser(UrBaseParser):
    _CONTAINER_CLASS_NAME: str = "c_container allparts"
    PARSED_OBJECT_TYPE_NAME: str = "PART"

    @staticmethod
    def _get_objects(
            items: List,
            depended_object: DependedObjectUrlModel,
    ) -> List[URPart]:
        parts = []
        for part_item in items:
            splitted_part = part_item.text.split(' - ', 1)
            if len(splitted_part) == 1:
                number, spec = splitted_part[0], ""
            else:
                number, spec = part_item.text.split(' - ', 1)
            parts.append(
                URPart(
                    number=number.strip(),
                    spec=spec.strip(),
                    name_of_model=depended_object.meta.get("model_name"),
                    category_name=depended_object.meta.get("category_name")
                )
            )
        return parts

    @staticmethod
    def _get_depended_urls_objects(
            items: List,
            depended_object: DependedObjectUrlModel
    ) -> List[DependedObjectUrlModel]:
        return []


