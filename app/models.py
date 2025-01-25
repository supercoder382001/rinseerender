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


class phone(BaseModel):
    mid: str
    muid: int
    amount: float
    mno: str
