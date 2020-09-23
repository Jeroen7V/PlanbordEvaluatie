FROM python:alpine

LABEL maintainer="Jeroen Vermeylen <jeroen@vermeylen.org>"

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && pip install --no-cache-dir uvicorn \
    && apk del .build-deps gcc libc-dev make
EXPOSE 8000

RUN pip install --no-cache-dir requests pydantic fastapi aiofiles jinja2 sqlalchemy

COPY ./src /src

RUN mkdir -p /src/db
VOLUME ["/src/db"]

CMD uvicorn --host 0.0.0.0 src.main:app