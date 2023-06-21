# IPSec Control Channel: Root CA Certificate Generation and Certificate Signing

The following guide offers step-by-step instructions on how to generate a root Certification Authority (CA) certificate for use in the IPSec Control Channel configuration. This root CA certificate will be used to sign certificates for the IPSec endpoints.

## Step 1: Generate the Root CA Certificate

1. Open a command prompt or terminal window.

2. Generate a private key for the root CA certificate:

    ```bash
    openssl genrsa -out root_ca.key 4096
    ```

   This command generates a 4096-bit RSA private key (root_ca.key).

3. Generate the self-signed root CA certificate:

    ```bash
    openssl req -new -x509 -sha256 -key root_ca.key -out root_ca.crt -days 3650
    ```

    This command creates a self-signed certificate (root_ca.crt) using the private key generated in the previous step.

    Provide the required information when prompted. The information typically includes the Common Name (CN), organization details, and other details related to your root CA.

    The root CA certificate (root_ca.crt) is now created and ready to be used to sign certificates for IPSec endpoints.

## Step 2: Generate IPSec Endpoint Certificates using a CSR

To generate certificates for the IPSec endpoints signed by the root CA certificate, follow these steps for each endpoint:

1. Generate a private key for the IPSec endpoint:

    ```bash
    openssl genrsa -out endpoint1.key 2048
    ```

    This command generates a 2048-bit RSA private key (endpoint1.key).

2. Create a Certificate Signing Request (CSR) file using the private key:

    ```bash
    openssl req -new -sha256 -key endpoint1.key -out endpoint1.csr
    ```

    This command creates a CSR file (endpoint1.csr) using the private key generated in the previous step.

    Enter the required information when prompted, including the Common Name (CN) and other details related to the IPSec endpoint.

3. Submit the CSR (endpoint1.csr) to the root CA for signing:

    ```bash
    openssl x509 -req -sha256 -in endpoint1.csr -CA root_ca.crt -CAkey root_ca.key -CAcreateserial -out endpoint1.crt -days 365
    ```

    This command signs the CSR using the root CA certificate (root_ca.crt) and private key (root_ca.key) and generates the signed certificate (endpoint1.crt) valid for 365 days.

Repeat steps 1-3 for each IPSec endpoint, generating a unique private key, CSR, and certificate for each.

The root CA has now signed the CSRs and provided you with the signed certificates (endpoint1.crt, endpoint2.crt, etc.) for each IPSec endpoint.
