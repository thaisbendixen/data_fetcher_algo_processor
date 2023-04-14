import os
import tempfile
from typing import Literal

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse

from app.common.models import ItemCollection, Request
from app.data_providers.dataset_handler import DatasetHandler

data_app = FastAPI()


def create_temp_file():
    fd, path = tempfile.mkstemp(suffix=".tif")
    with os.fdopen(fd, "w") as f:
        f.write("TEST\n")
    try:
        yield path
    finally:
        os.unlink(path)


@data_app.get("/")
def read_root():
    return {"Hello": "from data app"}


@data_app.post(
    "/search/{collection}",
    response_model=ItemCollection,
    description="Enables searching for available scenes in satellite collections "
    "(ex. sentinel-2) based on payload parameters (ex. datetime).",
)
async def search_data(
    collection: Literal["sentinel-2", "landsat-8"], request: Request
) -> ItemCollection:
    dataset_handler = DatasetHandler(collection=collection)
    return await dataset_handler.search_data(request=request)


@data_app.get(
    "/search/{collection}/{item_id}",
    description="Enables searching for specific scene from a satellite collection "
    "(ex. sentinel-2) based on item id.",
)
async def search_item(collection: Literal["sentinel-2", "landsat-8"], item_id: str):
    dataset_handler = DatasetHandler(collection=collection)
    return await dataset_handler.search_data(item_id=item_id)


@data_app.get(
    "/download/{collection}/{item_id}/tci",
    description="Enables downloading of True Color Image (TCI) of a "
    "specific scene from a satellite collection "
    "(ex. sentinel-2) based on item id.",
    response_class=FileResponse,
)
async def download_tci(
    collection: str, item_id: str, file_path=Depends(create_temp_file)
):
    dataset_handler = DatasetHandler(collection=collection)
    return await dataset_handler.download_tci(item_id=item_id, file_path=file_path)


@data_app.get(
    "/download/{collection}/{item_id}/band/{band_id}",
    description="Enables downloading a band of a specific scene from a "
    "satellite collection (ex. sentinel-2) based on item id.",
    response_class=FileResponse,
)
async def download_band(
    collection: Literal["sentinel-2", "landsat-8"],
    item_id: str,
    band_id: str,
    file_path=Depends(create_temp_file),
):
    dataset_handler = DatasetHandler(collection=collection)
    return await dataset_handler.download_band(
        item_id=item_id, band_id=band_id, file_path=file_path
    )
