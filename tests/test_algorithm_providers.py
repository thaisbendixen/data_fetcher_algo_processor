import os

import pytest
from fastapi.exceptions import HTTPException

from app.algorithm_providers.algorithms import NDVIProcessor


@pytest.mark.asyncio
async def test_get_bands():
    ...


@pytest.mark.skip(
    reason="Requires data app to be running"
)  # TODO add mocking of data app
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "algo_processor_class",
    [NDVIProcessor],
)
async def test_run(algo_processor_class, request_fixture):
    result = await algo_processor_class().run(
        collection="sentinel-2",
        item_id="S2A_33UUU_20180628_0_L2A",
        file_path="test.tif",
    )

    assert isinstance(result, str)
    os.path.isfile(result)
    os.unlink(result)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "algo_processor_class",
    [NDVIProcessor],
)
async def test_run_sample(algo_processor_class, request_fixture):
    result = await algo_processor_class().run(
        collection="sentinel-2", item_id="sample", file_path="test.png"
    )

    assert isinstance(result, str)
    os.path.isfile(result)
    os.unlink(result)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "algo_processor_class",
    [NDVIProcessor],
)
async def test_run_sample_error(algo_processor_class, request_fixture):
    with pytest.raises(HTTPException) as exc_info:
        await algo_processor_class().run(
            collection="landsat-8", item_id="sample", file_path="test.png"
        )
    assert (
        exc_info.value.detail
        == "Sample data currently only available for sentinel-2 collection ..."
    )
