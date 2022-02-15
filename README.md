# A webserver based on Tornado

The goal of this webserver is to receive files and to return a hash value for them.

## Setup

This project was written using Visual Studio Code.

You are encouraged to setup a virtual environment for this project:

    python -m venv .
    . bin/activate

You can install dependencies using the provided requirements file:

    pip install -r requirements.txt

## Building a docker image

    docker build -t hash_server -f docker/Dockerfile .

## Launching the server

With this project properly set up, do:

    python src/server.py [--port <port>]

With the docker image previously built:

    docker run --rm --name hash_server -p 8888:8888 hash_server

## Testing

The simplest way is to use curl to upload a file, using the command:

    curl -v -F upload=@README.md http://localhost:8888/upload

## Todo

Write a script to send multiple big files / random data at the same time to make sure the server properly handles asynchronism.
