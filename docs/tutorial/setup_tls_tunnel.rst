TLS Mutual Authenticated End-to-End Tunnel: Root CA Certificate Generation and Certificate Signing
==================================================================================================

This guide provides step-by-step instructions on how to generate a root Certification Authority (CA) certificate for use in the configuration of a TLS mutual authenticated end-to-end tunnel. This root CA certificate will be used to sign certificates for the TLS endpoints.

Step 1: Generate the Root CA Certificate
-----------------------------------------

1. Open a command prompt or terminal window.

2. Generate a private key for the root CA certificate:

   .. code-block:: bash

      openssl genrsa -out root_ca.key 4096

   This command generates a 4096-bit RSA private key (root_ca.key).

3. Generate the self-signed root CA certificate:

   .. code-block:: bash

      openssl req -new -x509 -sha256 -key root_ca.key -out root_ca.crt -days 3650

   This command creates a self-signed certificate (root_ca.crt) using the private key generated in the previous step.

   Provide the required information when prompted. The information typically includes the Common Name (CN), organization details, and other details related to your root CA.

   The root CA certificate (root_ca.crt) is now created and ready to be used to sign certificates for TLS endpoints.

Step 2: Generate TLS Endpoint Certificates using a CSR
------------------------------------------------------

To generate certificates for the TLS endpoints signed by the root CA certificate, follow these steps for each endpoint:

1. Generate a private key for the TLS endpoint:

   .. code-block:: bash

      openssl genrsa -out endpoint1.key 2048

   This command generates a 2048-bit RSA private key (endpoint1.key).

2. Create a Certificate Signing Request (CSR) file using the private key:

   .. code-block:: bash

      openssl req -new -sha256 -key endpoint1.key -out endpoint1.csr

   This command creates a CSR file (endpoint1.csr) using the private key generated in the previous step.

   Enter the required information when prompted, including the Common Name (CN) and other details related to the TLS endpoint.

   .. note::
   
      It is necessary to enter the Common Name (CN) accurately when generating the Certificate Signing Request (CSR) for each endpoint. Incorrect CN entry will lead to certificate validation issues and rejection by the other endpoint.

3. Submit the CSR (endpoint1.csr) to the root CA for signing:

   .. code-block:: bash

      openssl x509 -req -sha256 -in endpoint1.csr -CA root_ca.crt -CAkey root_ca.key -CAcreateserial -out endpoint1.crt -days 365

   This command signs the CSR using the root CA certificate (root_ca.crt) and private key (root_ca.key) and generates the signed certificate (endpoint1.crt) valid for 365 days.

4. Concatenate the private key and the certificate into one file:

   .. code-block:: bash

      cat endpoint1.key endpoint1.crt > endpoint1.pem

   This command combines the private key and the certificate into a single file (endpoint1.pem). This file will be used by the program that requires both in a single file.

Repeat steps 1-4 for each TLS endpoint, generating a unique private key, CSR, certificate, and combined PEM file for each.

The root CA has now signed the CSRs and provided you with the signed certificates (endpoint1.crt, endpoint2.crt, etc.) for each TLS endpoint.

Step 3: Configuration for Each Endpoint
---------------------------------------

With the root CA certificate and the endpoint's private certificate generated, you can configure each endpoint using a JSON configuration file, as shown below:

.. code-block:: json

   {
	"ROOT_CERTIFICATE": "root_ca.crt",
	"PRIVATE_CERTIFICATE": "endpoint1.pem",
	"DESTINATION_IP": "192.168.122.247",
	"SERVER_PORT": "443"
   }

Replace "endpoint1.pem" with the respective filename for each endpoint, and adjust "destination_ip" and "server_port" as necessary for your network configuration.
