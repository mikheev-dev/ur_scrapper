from typing import Any

import pydantic

from ur_objects_serializers.base_object_serializer import BaseSerializer


class PydanticSerializer(BaseSerializer):
    def serialize(self, obj: pydantic.BaseModel) -> str:
        return obj.model_dump_json()
