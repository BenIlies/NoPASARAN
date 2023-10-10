Configuring Certificate-Based Authentication for OpenSSH
========================================================

The SSH protocol provides various authentication options: passwords, public keys, and certificates. This tutorial will guide you through the steps to configure certificate-based authentication for an OpenSSH server.

How SSH Certificate-Based Authentication Works
----------------------------------------------

SSH certificates don't offer extra cryptography benefits beyond SSH public keys. The process involves setting up a certificate authority (CA). In OpenSSH, the CA certificate is a public and private key pair with added data. The CA's private key signs user and host certificates. For user authentication, the SSH client provides the user certificate to the SSH server during each new connection. The server verifies the certificate against the CA's public key.

Generating Certificate Authority (CA)
-------------------------------------

Generate the SSH CA keypair:

.. code-block:: bash

   ssh-keygen -t rsa -b 4096 -f host_ca

The ``host_ca`` file is the host CA's private key and should be protected. Best practices recommend generating separate CAs for signing host and user certificates.

Generate a ``user_ca``:

.. code-block:: bash

   ssh-keygen -t rsa -b 4096 -f user_ca

Issuing Host Certificates
-------------------------

Generate a new host key and sign it with the CA key:

.. code-block:: bash

   ssh-keygen -t rsa -b 4096 -f ssh_host_rsa_key
   ssh-keygen -s host_ca -I host.example-host.com -h -n host.example-host.com -V +52w ssh_host_rsa_key.pub

Explanation of flags:

- ``-s host_ca``: Specifies the CA private key for signing.
- ``-I host.example-host.com``: Cert's identity.
- ``-h``: Denotes a host certificate.
- ``-n host.example-host.com``: Specifies valid principals.
- ``-V +52w``: Defines validity for 52 weeks.

Configuring SSH to Use Host Certificates
----------------------------------------

Add this line to ``/etc/ssh/sshd_config``:

.. code-block:: bash

   HostCertificate /etc/ssh/ssh_host_rsa_key-cert.pub

Then, restart sshd:

.. code-block:: bash

   systemctl restart sshd

For the ssh client to use the certificate, append the CA's public key to the ``known_hosts`` file.

Issuing User Certificates
-------------------------

Generate a user key pair:

.. code-block:: bash

   ssh-keygen -t rsa -b 4096 -f user-key
   ssh-keygen -s user_ca -I username@nopasaran.com -n node-user,admin-user -V +1d user-key.pub

Explanation of flags:

- ``-s user_ca``: specifies the filename of the CA private key that should be used for signing.
- ``-I username@nopasaran.com``: the certificate's identity — a string that identifies the user. This is usually the user's email address or username.
- ``-n node-user,admin-user``: a comma-separated list of principals (usernames) that the certificate will be valid for authenticating as. 
- ``-V +1d``: specifies the validity period of the certificate — here, it's valid for one day from the moment of creation. Certificates for users should have a much shorter validity period than host certificates to reduce the risk associated with lost or stolen keys.

Configuring SSH to Use User Certificates
----------------------------------------

For user authentication, you'll add the CA's public key to the SSH server. Place it in a file under the `/etc/ssh` directory, set the permissions, and then add the following line to your `/etc/ssh/sshd_config` file:

.. code-block:: bash

    TrustedUserCAKeys /etc/ssh/user_ca.pub

Then, restart sshd:

.. code-block:: bash

    $ systemctl restart sshd

The server is now configured to trust any user certificate signed by `user_ca`.

Next, configure your SSH client to present your certificate when connecting. The simplest way to do this is to add an IdentityFile line pointing to your private key in your `~/.ssh/config` file:

.. code-block:: bash

    Host *.example-host.com
    IdentityFile ~/path/to/user-key

Now, whenever you connect to an SSH server as a user listed in the certificate (node-user or admin-user in this case), the client will automatically present your user certificate without you needing to specify it on the command line.

Now, you should be able to SSH into the server using certificate-based authentication. Ensure your certificate is not expired, and if you face any issues, you can debug using:

.. code-block:: bash

    $ ssh -vv [your-server] 2>&1 | grep certificate
