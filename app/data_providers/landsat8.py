import os
from typing import List, Literal, Optional

import boto3
import rasterio as rio
from fastapi.exceptions import HTTPException
from pystac_client import Client

from app.common.interfaces import DatasetFetcher
from app.common.models import ItemCollection, Request

# TODO few bands missing here
BAND_MAP = {
    "blue": "blue",
    "green": "green",
    "red": "red",
    "nir": "nir08",
    "swir1": "swir16",
    "swir2": "swir22",
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


class Landsat8DatasetFetcher(DatasetFetcher):
    @staticmethod
    async def search(
        request: Optional[Request] = None, item_id: Optional = None
    ) -> ItemCollection:
        if item_id:
            try:
                landsat_stac_client = Client.open(
                    "https://landsatlook.usgs.gov/stac-server", headers=[]
                )
                search = landsat_stac_client.search(
                    ids=[item_id], collections=["landsat-c2l2-sr"]
                )

            except Exception as e:
                raise HTTPException(400, detail=e.__repr__())

        else:
            try:
                landsat_stac_client = Client.open(
                    "https://landsatlook.usgs.gov/stac-server", headers=[]
                )
                search = landsat_stac_client.search(
                    intersects=request.intersects,
                    datetime=request.datetime,
                    collections=["landsat-c2l2-sr"],
                )

            except Exception as e:
                raise HTTPException(400, detail=e.__repr__())

        return ItemCollection(**search.item_collection_as_dict())

    async def download_tci(self, item_id: str, file_path: str) -> str:
        raise NotImplementedError

    async def download_band(
        self,
        item_id: str,
        band_id: List[Literal["blue", "green", "red", "nir08", "swir16", "swir22"]],
        file_path: str,
    ) -> str:
        breakpoint()
        if not item_id:
            raise Exception()

        item_collection = await self.search(item_id=item_id)
        band_name = BAND_MAP.get(band_id)
        band_href = item_collection.features[0].assets[band_name]["href"]

        breakpoint()
        open_write_href(href=band_href, file_path=file_path)

        breakpoint()
        return file_path
