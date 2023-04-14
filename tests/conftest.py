import pytest
from shapely.geometry import Polygon

from app.common.models import Credentials, Request


@pytest.fixture
def credentials():
    return Credentials(account_id="some account id", password="some key")


@pytest.fixture
def geom():
    return {
        "type": "Polygon",
        "coordinates": [
            [
                [13.205264482787868, 52.53399625652757],
                [13.201874500639157, 52.53035726947937],
                [13.197086887762731, 52.531700552397666],
                [13.197084126899975, 52.53176794506914],
                [13.201488372876756, 52.53601584214123],
                [13.201488580428844, 52.53601584529632],
                [13.205264482787868, 52.53399625652757],
            ]
        ],
    }


@pytest.fixture
def geojson_geom(geom):
    poly = Polygon(geom["coordinates"])
    return poly


@pytest.fixture
def request_fixture(credentials, geom):
    return Request(
        credentials=credentials,
        intersects=geom,
        datetime="2017-06-01T00:00:00Z/2018-06-30T23:59:59Z",
    )
