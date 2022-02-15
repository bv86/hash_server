FROM python:alpine3.15

WORKDIR /src

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY src/ ./

CMD [ "python", "server.py" ]

