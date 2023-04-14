import os

import pytest

from app.common.models import ItemCollection
from app.data_providers.landsat8 import Landsat8DatasetFetcher
from app.data_providers.sentinel2 import Sentinel2DatasetFetcher


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_fetcher_class, href",
    [
        [
            Sentinel2DatasetFetcher,
            "https://earth-search.aws.element84.com/v0/collections"
            "/sentinel-s2-l2a-cogs",
        ],
        [
            Landsat8DatasetFetcher,
            "https://landsatlook.usgs.gov/stac-server/collections"
            "/landsat-c2l2-sr/items/",
        ],
    ],
)
async def test_search(data_fetcher_class, href, request_fixture):
    result = await data_fetcher_class().search(request=request_fixture)

    assert isinstance(result, ItemCollection)
    assert href in result.features[0].links[0]["href"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_fetcher_class, item_id",
    [
        [Sentinel2DatasetFetcher, "S2A_33UUU_20180628_0_L2A"],
        [Landsat8DatasetFetcher, "LE07_L2SP_193023_20180629_20200829_02_T1_SR"],
    ],
)
async def test_search_item_id(data_fetcher_class, item_id, request_fixture):
    result = await data_fetcher_class().search(item_id=item_id)

    assert isinstance(result, ItemCollection)
    assert len(result.features) == 1
    assert result.features[0].id == item_id


@pytest.mark.skip(reason="Avoid download because of limited internet access")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_fetcher_class, item_id",
    [
        [Sentinel2DatasetFetcher, "S2A_33UUU_20180628_0_L2A"],
    ],
)
async def test_download_tci(data_fetcher_class, item_id, request_fixture):
    result = await data_fetcher_class().download_tci(
        item_id=item_id, file_path="test.tif"
    )

    assert isinstance(result, str)
    os.path.isfile(result)
    os.unlink(result)


@pytest.mark.skip(reason="Avoid download because of limited internet access")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_fetcher_class, item_id",
    [
        [Sentinel2DatasetFetcher, "S2A_33UUU_20180628_0_L2A"],
        [Landsat8DatasetFetcher, "LE07_L2SP_193023_20180629_20200829_02_T1_SR"],
    ],
)
async def test_download_band(data_fetcher_class, item_id, request_fixture):
    result = await data_fetcher_class().download_band(
        item_id=item_id, band_id="red", file_path="test.tif"
    )

    assert isinstance(result, str)
    os.path.isfile(result)
    os.unlink(result)
