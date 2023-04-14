import abc
from abc import ABC
from typing import List, Literal, Optional

import numpy as np
from satstac.itemcollection import ItemCollection

from app.common.models import Request


class DatasetFetcher(ABC):
    """Defines the interface for the dataset fetcher classes."""

    @staticmethod
    @abc.abstractmethod
    async def search(
        request: Optional[Request] = None, item_id: Optional = None
    ) -> ItemCollection:
        """
        Based on user defined parameters, example datatime and AOI, searches the dataset
        API for available images. A STAC compliant item collection, with all search
        results, is returned.
        """

    @abc.abstractmethod
    async def download_tci(self, item_id: str, file_path: str) -> str:
        """
        Downloads True Color Image (TCI) and saves file in an output file path.
        """

    @abc.abstractmethod
    async def download_band(self, item_id: str, band_id: str, file_path: str) -> str:
        """
        Downloads band based on a band id and saves file in an output file path.
        """


class AlgoProcessor(ABC):
    """Defines the interface for the algorithm processor classes"""

    @staticmethod
    @abc.abstractmethod
    async def get_bands(
        collection: Literal["sentinel-2", "landsat-8"], item_id: str
    ) -> List[np.ndarray]:
        """
        Downloads bands from chosen scene using secondary data app service
        (http://0.0.0.0:8085) and returns the bands in a list of band arrays.
        """

    @staticmethod
    @abc.abstractmethod
    async def create_png(array: np.array, file_path: str):
        """
        Creates and stores PNG from array.
        """

    @abc.abstractmethod
    async def run(
        self,
        collection: Literal["sentinel-2", "landsat-8"],
        item_id: str,
        file_path: str,
    ) -> str:
        """
        Runs algorithm on chosen scene, based on item id and a sensor collection
        (ex. sentinel-2), and stores output as PNG.
        """
