from concurrent.futures import ThreadPoolExecutor

import uvicorn

from app.config import AlgoAppSettings, DataAppSettings
from app.services.algo_app import algo_app
from app.services.data_app import data_app

data_app_config = uvicorn.Config(
    data_app, host=DataAppSettings().url.host, port=int(DataAppSettings().url.port)
)

algo_app_config = uvicorn.Config(
    algo_app,
    host=DataAppSettings().url.host,
    port=int(AlgoAppSettings().url.port),
)


servers = [
    uvicorn.Server(config=data_app_config),
    uvicorn.Server(config=algo_app_config),
]

with ThreadPoolExecutor(max_workers=len(servers)) as pool:
    for server in servers:
        pool.submit(server.run)
