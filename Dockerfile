FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y nano iputils-ping git python3 wget

RUN wget -O - https://bootstrap.pypa.io/get-pip.py | python3

RUN git clone https://github.com/BenIlies/NoPASARAN.git

WORKDIR /NoPASARAN

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt