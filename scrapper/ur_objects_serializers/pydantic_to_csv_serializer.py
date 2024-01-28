from pydantic import BaseModel
from typing import List

from scrapper.ur_objects_serializers.base_object_serializer import BaseSerializer


class PydanticToCSVSerializer(BaseSerializer):
    _fields_order: List[str]
    _d_sym: str

    def __init__(self, fields_order: List[str], d_sym: str = '\t'):
        self._fields_order = fields_order
        self._d_sym = d_sym

    def serialize(self, obj: BaseModel) -> str:
        obj_json = obj.model_dump()
        return self._d_sym.join([
            obj_json.get(field, '')
            for field in self._fields_order
        ])
