<!-- ABOUT THE PROJECT -->
# Open source data fetcher and algorithm runner

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#project-description">Project description</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#usage">Usage</a></li>
   <li><a href="#developers">Developers</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>



<!-- PROJECT DESCRIPTION -->
## Project Description

Creates two APIs responsible for fetching and processing open source satellite data (ex. Sentinel-2 or Landat8). The
data API can be extended with new datasets/sensors, currently only Sentinel-2 and Landsat8 are provided. The algorithm API,
currently only provides NDVI algorithm but can also be extended. Please be aware that this repo is a
work and progress. Refer to <a href="#roadmap">Roadmap</a> to see next steps for project.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To setup your work environment and run the code please follow the instructions below.

<!-- PRE-REQUISITES -->
### Pre-requisites
For running this code you will need the following tools:
* Python ^3.9.
* [Docker](https://docs.docker.com/get-docker/)

I recommend using a python version manager (ex. [pyenv](https://github.com/pyenv/pyenv)) and a virtual environment
manager (ex. [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)).

### Optional requisites

The data API relies on AWS, which means you need to have AWS credentials. If you don't want to create AWS credentials,
your access to the APIs will be restricted to search and running algorithms on sample data. Information on how to
create an account can be found [here]([pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv))). You'll need
to store your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in the [.env dile](.env) for running the APIs with Docker.
If you are a developer make sure to also add them to your local environment variables. For creating the AWS
credentials I found [this](https://stackoverflow.com/questions/21440709/how-do-i-get-aws-access-key-id-for-amazon)
stackoverflow thread helpful.

### Installation

The steps below are only required if you would like to run the code on your local machine outside the docker
container. If you wish to only run the code within the docker container, please skip the steps below.

Install poetry (see documentation [here](https://python-poetry.org/docs/)):
   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   ```
To install the defined dependencies for your project run:
   ```sh
   poetry install --without dev
   ```

### Installation for developers
Install development dependencies packages:
   ```sh
   poetry install
   ```

Install [pre-commit hook](https://pre-commit.com/) and existing pre-commit file (required github account and CLI):
   ```sh
   brew install pre-commit
   pre-commit install
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

To containerise the services and all Its dependencies we used [Docker](https://docs.docker.com/get-docker/).
We will use `docker-compose up` which orchestrates multiple containers for our APIs.

To build and run the containers:
   ```sh
   docker-compose up
   ```

Use your favourite API client (ex. [Postman](https://www.postman.com/)) to connect to the APIs and find the
swagger documentation in http://localhost:8085/ and http://0.0.0.0:8086/docs.

Please find the url mappings of the available APIs below:

- Data API: http://localhost:8085/
- Algorithm API: http://localhost:8086/

#### Without AWS credentials

If you **don't have AWS credentials** you won't be able to download data. Therefore, you will be restricted searching
with the Data API and running algorithms only on sentinel-2 sample data. See examples:

Example search:
   ```sh
   curl --location 'http://0.0.0.0:8085/search/sentinel-2' \
   --header 'Content-Type: application/json' \
   --data '{
       "credentials": {
           "account_id": "some account id",
           "password": "some key"
       },
       "intersects": {
           "type": "Polygon",
           "coordinates": [
               [
                   [
                       13.205264482787868,
                       52.53399625652757
                   ],
                   [
                       13.201874500639157,
                       52.53035726947937
                   ],
                   [
                       13.197086887762731,
                       52.531700552397666
                   ],
                   [
                       13.197084126899975,
                       52.53176794506914
                   ],
                   [
                       13.201488372876756,
                       52.53601584214123
                   ],
                   [
                       13.201488580428844,
                       52.53601584529632
                   ],
                   [
                       13.205264482787868,
                       52.53399625652757
                   ]
               ]
           ]
       },
       "datetime": "2019-06-01T00:00:00Z/2020-06-30T23:59:59Z"
   }'
   ```

Example of running algorithm on sample data:
   ```sh
   curl --location 'http://0.0.0.0:8086/sentinel-2/sample/ndvi' \
    --output 's2_sample_NDVI.png'
   ```

#### With AWS credentials

If you **have AWS credentials** you can search and download data, as well as run algorithms on top of data. See below:

Example search:
   ```sh
   curl --location 'http://0.0.0.0:8085/search/sentinel-2' \
   --header 'Content-Type: application/json' \
   --data '{
       "credentials": {
           "account_id": "some account id",
           "password": "some key"
       },
       "intersects": {
           "type": "Polygon",
           "coordinates": [
               [
                   [
                       13.205264482787868,
                       52.53399625652757
                   ],
                   [
                       13.201874500639157,
                       52.53035726947937
                   ],
                   [
                       13.197086887762731,
                       52.531700552397666
                   ],
                   [
                       13.197084126899975,
                       52.53176794506914
                   ],
                   [
                       13.201488372876756,
                       52.53601584214123
                   ],
                   [
                       13.201488580428844,
                       52.53601584529632
                   ],
                   [
                       13.205264482787868,
                       52.53399625652757
                   ]
               ]
           ]
       },
       "datetime": "2017-06-01T00:00:00Z/2018-06-30T23:59:59Z"
   }'
   ```
Each
search returns a FeatureCollection, where each Feature has an id. This id can be used to download or run algorithms
on specific scenes:

Example download True Color Image:
   ```sh
   curl --location 'http://0.0.0.0:8085/download/sentinel-2/S2A_33UUU_20180628_0_L2A/tci' \
    --output 's2_TCI.tif'
   ```

Example running NDVI on specific sentinel-2 scene:
   ```sh
   curl --location 'http://0.0.0.0:8086/sentinel-2/S2A_33UUU_20180628_0_L2A/ndvi' \
    --output 's2_NDVI.png'
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- DEVELOPERS -->
## Developers

This code base already included a few unit test, but more tests, including mock tests, should be added when possible.
Please be aware the tests are live test, which are making requests to a provider API, they will fail if
AWS credentials are not setup.

Run APIs on local machine:
   ```sh
   python -m app
   ```

To run pytest:
   ```sh
   python -m pytest
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Add and improve exception handling
- [ ] Add mock tests
- [ ] Add more tests (ex. tests for each endpoint, tests for exceptions and tests with different params)
- [ ] Add logger statements
- [ ] Run mypy on code
- [ ] Reduce size of inflated Docker image, which is almost 2GB (by reducing dependencies for example)
- [ ] Improve response speed of endpoints
- [ ] Enable clipping scenes
- [ ] Find better solution to avoid saving files (see [here](https://github.com/thaisbendixen/data_fetcher_algo_processor/blob/63190da26449d4fcb5b5545d06c7f4318cedcb22/app/services/algo_app.py#L13) and [here](https://github.com/thaisbendixen/data_fetcher_algo_processor/blob/63190da26449d4fcb5b5545d06c7f4318cedcb22/app/services/data_app.py#L14))

<p align="right">(<a href="#readme-top">back to top</a>)</p>
