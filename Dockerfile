FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y nano iputils-ping git python3 wget

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN wget -O - https://bootstrap.pypa.io/get-pip.py | python

RUN git clone https://github.com/BenIlies/NoPASARAN.git

WORKDIR /NoPASARAN

COPY requirements.txt .

RUN python -m pip install -r requirements.txt
