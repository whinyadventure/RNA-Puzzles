# Dockerfile
FROM python:3.6.7-alpine3.7

RUN mkdir -p /code

WORKDIR /code

# Annotate Port
EXPOSE 3000

# System Deps
RUN apk update && \
    apk add --no-cache \
        gcc \
        musl-dev \
        libc-dev \
        linux-headers \
        postgresql-dev \
	zlib \
        jpeg-dev \
       zlib-dev \
       freetype-dev \
       lcms2-dev \
       openjpeg-dev \
       tiff-dev \
       tk-dev \
       tcl-dev \
       harfbuzz-dev \
       fribidi-dev

# Java
RUN apk fetch openjdk8
RUN apk add openjdk8

# Python Application Deps
COPY requirements.txt .
RUN pip install -r requirements.txt

# We'll use Gunicorn to run our app
RUN pip install gunicorn

# Application Setup
COPY RNAPuzzles ./RNAPuzzles/

WORKDIR /code/RNAPuzzles



ENTRYPOINT ["gunicorn"]
CMD ["RNAPuzzles.wsgi:application"]

