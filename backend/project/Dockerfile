# pull official base image
FROM --platform=linux/amd64 python:3.11.2-slim-buster

# set working directory
RUN mkdir -p /build
WORKDIR /build

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /build/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/build/entrypoint.sh"]