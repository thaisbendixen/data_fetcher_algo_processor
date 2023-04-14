from typing import Literal, Optional

from fastapi.exceptions import HTTPException

from app.common.models import ItemCollection, Request
from app.data_providers.landsat8 import Landsat8DatasetFetcher
from app.data_providers.sentinel2 import Sentinel2DatasetFetcher

DATASET_MAP = {
    "sentinel-2": Sentinel2DatasetFetcher,
    "landsat8": Landsat8DatasetFetcher,
}


class DatasetHandler:
    def __init__(self, collection: Literal["sentinel-2", "landsat-8"]):
        self.collection = collection
        self.dataset_class = DATASET_MAP.get(self.collection)

    async def search_data(
        self, request: Optional[Request] = None, item_id: Optional[str] = None
    ) -> ItemCollection:
        if not item_id and not request:
            raise HTTPException(
                400, detail="Either item_id or search request payload are required ..."
            )
        dataset_init = self.dataset_class()
        return await dataset_init.search(request=request, item_id=item_id)

    async def download_tci(self, item_id: str, file_path: str) -> str:
        dataset_init = self.dataset_class()
        return await dataset_init.download_tci(item_id=item_id, file_path=file_path)

    async def download_band(self, item_id: str, band_id: str, file_path: str) -> str:
        dataset_init = self.dataset_class()
        return await dataset_init.download_band(
            item_id=item_id, band_id=band_id, file_path=file_path
        )
