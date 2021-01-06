# pull official base image
FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1
# set working directory
WORKDIR /usr/src/app

# install python dependencies
RUN python -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

# add app
COPY . .
