import pytest

from scrapper.ur_objects_serializers import PydanticToCSVSerializer
from scrapper.ur_models import URPart


@pytest.mark.parametrize("delimiter", [',', None])
def test_pydantic_to_csv_serializer(delimiter):
    fields_order = [
        "category_name",
        "spec",
        "number",
        "name_of_model"
    ]
    obj = URPart(
        number="number1",
        spec="spec2",
        name_of_model="model3",
        category_name="category4",
    )

    init_dict = {
        "fields_order": fields_order,
    }
    if delimiter:
        init_dict["d_sym"] = delimiter
    serializer = PydanticToCSVSerializer(**init_dict)

    result = serializer.serialize(obj)

    splitted_result = result.split(delimiter if delimiter else '\t')

    assert len(splitted_result) == 4
    assert splitted_result == [
        "category4", "spec2", "number1", "model3"
    ]
