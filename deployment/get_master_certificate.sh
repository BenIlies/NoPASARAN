#!/bin/bash

# Set the domain name of the master for which we want to obtain the certificate
DOMAIN="master.nopasaran.org"

# Set the email address for Let's Encrypt notifications
EMAIL="ilies.benhabbour@kaust.edu.sa"

# Ensure Certbot is installed
if ! command -v certbot &>/dev/null; then
  echo "Certbot is not installed. Please install Certbot first."
  exit 1
fi

# Obtain the SSL/TLS certificate using Certbot
certbot certonly --standalone -d "$DOMAIN" --email "$EMAIL" --agree-tos