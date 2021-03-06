# pull official base image
FROM python:3

# set environment variables
ENV PYTHONUNBUFFERED 1

# set work directory
RUN mkdir /code
WORKDIR /code

# install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# copy project
COPY . /code/

# run docker-entrypoint.sh
ENTRYPOINT ["/code/docker-entrypoint.sh"]