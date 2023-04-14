import os
import tempfile
from typing import Literal

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse

from app.algorithm_providers.algorithm_handler import AlgoHandler

algo_app = FastAPI()


def create_temp_file():
    fd, path = tempfile.mkstemp(suffix=".png")
    with os.fdopen(fd, "w") as f:
        f.write("TEST\n")
    try:
        yield path
    finally:
        os.unlink(path)


@algo_app.get("/")
def read_root():
    return {"Hello": "from algo app"}


@algo_app.get(
    "/{collection}/{item_id}/{algo}",
    description="Runs algorithms (ex. NDVI) on specific scene and outputs PNG file.",
    response_class=FileResponse,
)
async def run_algorithm(
    collection: Literal["sentinel-2", "landsat-8"],
    item_id: str,
    algo: Literal["ndvi", "ndwi"],
    file_path=Depends(create_temp_file),
):
    algo_handler = AlgoHandler(algo=algo)
    return await algo_handler.run(
        collection=collection, item_id=item_id, file_path=file_path
    )
