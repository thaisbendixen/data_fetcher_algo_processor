from typing import List, Literal

import matplotlib.pyplot as plt
import numpy as np
import rasterio as rio
import requests
from fastapi.exceptions import HTTPException

from app.common.interfaces import AlgoProcessor
from app.config import DataAppSettings

np.seterr(divide="ignore", invalid="ignore")


class NDVIProcessor(AlgoProcessor):
    @staticmethod
    async def get_bands(
        collection: Literal["sentinel-2", "landsat-8"], item_id: str
    ) -> List[np.ndarray]:
        list_arrays = []
        if item_id == "sample":
            if collection != "sentinel-2":
                raise HTTPException(
                    400,
                    detail="Sample data currently only available "
                    "for sentinel-2 collection ...",
                )

            for path in [
                "./tests/sample_data/sentinel2_B04.tif",
                "./tests/sample_data/sentinel2_B08.tif",
            ]:
                with rio.open(path) as src:
                    array = src.read()
                    list_arrays.append(array)
        else:
            for url in [
                f"/download/{collection}/{item_id}/band/red",
                f"/download/{collection}/{item_id}/band/nir",
            ]:
                band_url = DataAppSettings().url + url
                response = await requests.get(band_url)
                file = response.content
                with rio.open(file) as src:
                    array = src.read()
                    list_arrays.append(array)

        return list_arrays

    @staticmethod
    def create_png(array: np.array, file_path: str):
        arr = np.moveaxis(array, 0, -1)

        min = np.nanmin(arr)
        max = np.nanmax(arr)

        colormap = plt.cm.RdYlGn

        fig = plt.figure(figsize=(20, 10))

        ax = fig.add_subplot(111)
        ax.axis("off")
        ax.set_title(
            "Normalized Difference Vegetation Index (NDVI)",
            fontsize=17,
            fontweight="bold",
        )

        cbar_plot = ax.imshow(arr, cmap=colormap, vmin=min, vmax=max)
        fig.colorbar(cbar_plot, orientation="horizontal", shrink=0.65)

        fig.savefig(file_path, dpi=200, bbox_inches="tight", pad_inches=0.7)

    async def run(
        self,
        collection: Literal["sentinel-2", "landsat-8"],
        item_id: str,
        file_path: str,
    ) -> str:
        list_arrays = await self.get_bands(collection=collection, item_id=item_id)
        red_array = list_arrays[0]
        nir_array = list_arrays[1]

        ndvi_array = (nir_array.astype(float) - red_array.astype(float)) / (
            nir_array + red_array
        )

        self.create_png(array=ndvi_array, file_path=file_path)

        return file_path


class NDWIProcessor(AlgoProcessor):
    @staticmethod
    async def get_bands(
        collection: Literal["sentinel-2", "landsat-8"], item_id: str
    ) -> List[np.ndarray]:
        raise NotImplementedError

    @staticmethod
    def create_png(array: np.array, file_path: str):
        raise NotImplementedError

    async def run(
        self,
        collection: Literal["sentinel-2", "landsat-8"],
        item_id: str,
        file_path: str,
    ) -> str:
        raise NotImplementedError
