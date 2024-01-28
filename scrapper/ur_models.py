from pydantic import BaseModel
from typing import List, Dict, Any


class URPart(BaseModel):
    number: str
    spec: str
    name_of_model: str
    category_name: str


class URModel(BaseModel):
    name: str
    manufacturer_name: str


class URCategory(BaseModel):
    name: str


class URManufacturer(BaseModel):
    name: str


class DependedObjectUrlModel(BaseModel):
    url: str
    meta: Dict[str, Any]
