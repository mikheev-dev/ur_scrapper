import pydantic

from scrapper.ur_objects_serializers.base_object_serializer import BaseSerializer


class PydanticSerializer(BaseSerializer):
    def serialize(self, obj: pydantic.BaseModel) -> str:
        return obj.model_dump_json()
