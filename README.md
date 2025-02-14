# Minimal FastAPI App


A minimal app developed with [FastAPI](https://fastapi.tiangolo.com/) framework.

The main purpose is to introduce how to implement the REST APIs with FastAPI


## How to deploy & run for the _Development_ env

- Make sure you have python - `Python 3.10.16`
- Create virtual environment `python3 -m venv venv`
- Activate the venv `source venv/bin/activate`
- Install requirements: `pip3 install -r requirements.txt`
- Makefile is provided need to just run `make run-dev` in CMD which spin up the server


## How to deploy & run for the _Production_ env

- Build the Image `make build`
- Spin the Container `make run`
