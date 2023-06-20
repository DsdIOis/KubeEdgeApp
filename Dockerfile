FROM ubuntu:20.04

ENV PYTHONBUFFERED 1
RUN mkdir /app

WORKDIR /app

RUN apt-get update

# Install python
RUN apt-get install python3 -y
# Install pip for python packages
RUN apt-get install python3-pip -y
# Install requirements
COPY requirements.txt /app/
RUN python3 -m pip install -r requirements.txt

COPY . /app/

CMD ["python3", "./mqtt_publisher.py"]
