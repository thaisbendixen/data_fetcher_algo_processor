from typing import List, Literal, Optional

from geojson_pydantic.geometries import Geometry
from geojson_pydantic.types import BBox
from pydantic import BaseModel, Extra


class Credentials(BaseModel):
    account_id: Optional[str] = None
    password: str

    class Config:
        extra = Extra.ignore


class Request(BaseModel):
    credentials: Optional[Credentials] = None
    intersects: dict
    datetime: str


class Item(BaseModel):
    type: Literal["Feature"]
    stac_version: str
    id: str
    bbox: BBox
    geometry: Geometry
    collection: Literal["sentinel-s2-l2a-cogs", "landsat-c2l2-sr"]
    assets: dict
    links: List[dict]

    class Config:
        extra = Extra.ignore


class ItemCollection(BaseModel):
    type: Literal["FeatureCollection"]
    features: List[Item]

    class Config:
        extra = Extra.ignore
