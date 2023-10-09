#!/bin/bash

# Set the domain name for which we want to obtain the certificate
DOMAIN="www.nopasaran.org"

# Set the email address for Let's Encrypt notifications
EMAIL="ilies.benhabbour@kaust.edu.sa"

# Set the output directory
OUTPUT_DIR="deployment/project_web_pki"

# Ensure OpenSSL is installed
if ! command -v openssl &>/dev/null; then
  echo "OpenSSL is not installed. Please install OpenSSL first."
  exit 1
fi

# Delete the existing content of the output directory and create a clean one
rm -rf "$OUTPUT_DIR" && mkdir "$OUTPUT_DIR"

# Generate a private key without encryption
openssl genpkey -algorithm RSA -out "$OUTPUT_DIR/$DOMAIN.key" -outform PEM

# Generate a CSR (Certificate Signing Request)
openssl req -new -key "$OUTPUT_DIR/$DOMAIN.key" -out "$OUTPUT_DIR/$DOMAIN.csr" -subj "/CN=$DOMAIN"

# Ensure Certbot is installed
if ! command -v certbot &>/dev/null; then
  echo "Certbot is not installed. Please install Certbot first."
  exit 1
fi

# Define custom paths for the full chain, intermediate chain, and certificate
FULLCHAIN_PATH="$OUTPUT_DIR/$DOMAIN.fullchain.crt"
CHAIN_PATH="$OUTPUT_DIR/$DOMAIN.chain.crt"
CERT_PATH="$OUTPUT_DIR/$DOMAIN.crt"

# Obtain the SSL/TLS certificate using Certbot and specify the CSR and custom certificate paths
certbot certonly --standalone -d "$DOMAIN" --csr "$OUTPUT_DIR/$DOMAIN.csr" --cert-path "$CERT_PATH" --fullchain-path "$FULLCHAIN_PATH" --chain-path "$CHAIN_PATH" --email "$EMAIL" --agree-tos
