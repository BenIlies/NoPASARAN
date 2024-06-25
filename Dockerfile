FROM ubuntu:latest

# Update and upgrade packages
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y nano iputils-ping git python3 wget libpcap-dev python3-venv

# Create a directory for your application
WORKDIR /app

# Create a virtual environment
RUN python3 -m venv venv

# Make sure we use the virtual environment's Python
ENV PATH="/app/venv/bin:$PATH"

# Update pip and install necessary packages
RUN python -m pip install --upgrade pip && \
    python -m pip install nopasaran
