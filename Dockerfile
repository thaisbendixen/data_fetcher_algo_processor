FROM python:3.9.10

WORKDIR app

COPY app/ .
COPY poetry.lock .
COPY pyproject.toml .

# hack to solve "[Errno 2] No such file or directory: 'gdal-config'"
RUN apt-get update
RUN apt-get install -y libgdal-dev
RUN pip install GDAL==3.2.2.1


RUN pip install poetry && \
    poetry config --local installer.no-binary rasterio && \
    poetry config virtualenvs.create false && \
    poetry install

CMD ["python", "-m", "app"]
