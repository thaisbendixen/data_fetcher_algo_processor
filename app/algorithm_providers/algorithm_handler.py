from typing import Literal

from app.algorithm_providers.algorithms import NDVIProcessor, NDWIProcessor

ALGO_MAP = {
    "ndvi": NDVIProcessor,
    "ndwi": NDWIProcessor,
}


class AlgoHandler:
    def __init__(self, algo: Literal["ndvi", "ndwi"]):
        self.algo = algo
        self.algo_class = ALGO_MAP.get(self.algo)

    def run(
        self,
        collection: Literal["sentinel-2", "landsat-8"],
        item_id: str,
        file_path: str,
    ) -> str:
        algo_init = self.algo_class()
        return algo_init.run(
            collection=collection, item_id=item_id, file_path=file_path
        )
