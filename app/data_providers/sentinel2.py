import logging
import os
from typing import List, Literal, Optional

import boto3
import certifi
import rasterio as rio
import satsearch
from fastapi.exceptions import HTTPException

from app.common.interfaces import DatasetFetcher
from app.common.models import ItemCollection, Request

logger = logging.getLogger(__name__)


os.environ[
    "CURL_CA_BUNDLE"
] = certifi.where()  # certificate path necessary for fetching href with rasterio


BAND_MAP = {
    "coastal": "B01",
    "blue": "B02",
    "green": "B03",
    "red": "B04",
    "vnir1": "B05",
    "vnir2": "B06",
    "vnir3": "B07",
    "nir": "B08",
    "water vapour": "B09",
    "swir cirrus": "B10",
    "swir": "B11",
    "swir2": "B12",
}


def open_write_href(href: str, file_path: str):
    aws_session = rio.session.AWSSession(
        boto3.Session(),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    with rio.Env(aws_session):
        with rio.open(href) as src:
            band_array = src.read()
            profile = src.profile
            with rio.open(file_path, "w", **profile) as dst:
                dst.write(band_array)


class Sentinel2DatasetFetcher(DatasetFetcher):
    @staticmethod
    async def search(
        request: Optional[Request] = None, item_id: Optional = None
    ) -> ItemCollection:
        if item_id:
            try:
                search = satsearch.Search.search(
                    url="https://earth-search.aws.element84.com/v0",
                    ids=[item_id],
                    collections=["sentinel-s2-l2a-cogs"],
                )
                search_items = search.items()

            except Exception as e:
                raise HTTPException(400, detail=e.__repr__())

        else:
            try:
                search = satsearch.Search.search(
                    url="https://earth-search.aws.element84.com/v0",
                    intersects=request.intersects,
                    datetime=request.datetime,
                    collections=["sentinel-s2-l2a-cogs"],
                )
                search_items = search.items()

            except Exception as e:
                raise HTTPException(400, detail=e.__repr__())

        return ItemCollection(**search_items.geojson())

    async def download_tci(self, item_id: str, file_path: str) -> str:
        item_collection = await self.search(item_id=item_id)
        tci_href = item_collection.features[0].assets["visual"]["href"]
        open_write_href(href=tci_href, file_path=file_path)

        return file_path

    async def download_band(
        self,
        item_id: str,
        band_id: List[
            Literal[
                "coastal",
                "blue",
                "green",
                "red",
                "vnir1",
                "vnir2",
                "vnir3",
                "nir",
                "water vapour",
                "swir cirrus",
                "swir",
                "swir2",
            ]
        ],
        file_path: str,
    ):
        item_collection = await self.search(item_id=item_id)
        band_name = BAND_MAP.get(band_id)
        band_href = item_collection.features[0].assets[band_name]["href"]

        open_write_href(href=band_href, file_path=file_path)

        return file_path
