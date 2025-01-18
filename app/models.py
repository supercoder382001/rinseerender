from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    name: str


class latlang(BaseModel):
    latitude: str
    longitude: str


class total(BaseModel):
    latitude: str
    longitude: str
    name: str
    method:int
