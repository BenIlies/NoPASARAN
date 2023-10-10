Configuring Certificate-Based Authentication for OpenSSH
========================================================

The SSH protocol provides various authentication options: passwords, public keys, and certificates. This tutorial will guide you through the steps to configure certificate-based authentication for an OpenSSH server.

How SSH Certificate-Based Authentication Works
----------------------------------------------

SSH certificates don't offer extra cryptography benefits beyond SSH public keys. Instead, they streamline the process of managing public keys. The SSH server only needs to trust the Certificate Authority (CA) rather than every user's public key. 

For SSH, a CA is a trusted entity that signs user and host certificates. The SSH client provides its certificate to the SSH server during connection, which the server then verifies against the CA's public key. Likewise, the SSH server provides its certificate to the client for verification.

Generating Certificate Authority (CA)
-------------------------------------

Generate the SSH CA keypair:

.. code-block:: bash

   ssh-keygen -t rsa -b 4096 -f host_ca

This command generates a private key ``host_ca`` and a public key ``host_ca.pub``. The private key should be kept secure.

Best practices recommend using separate CAs for hosts and users:

.. code-block:: bash

   ssh-keygen -t rsa -b 4096 -f user_ca

This generates a private key ``user_ca`` and its corresponding public key ``user_ca.pub``.

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

1. **On the SSH server**:

Add this line to ``/etc/ssh/sshd_config``:

.. code-block:: bash

   HostCertificate /etc/ssh/ssh_host_rsa_key-cert.pub

Then, restart sshd:

.. code-block:: bash

   systemctl restart sshd

2. **On the SSH client**:

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

1. **On the SSH server**:

For user authentication, you'll add the CA's public key to the SSH server. Place it in a file under the `/etc/ssh` directory, set the permissions, and then add the following line to your `/etc/ssh/sshd_config` file:

.. code-block:: bash

    TrustedUserCAKeys /etc/ssh/user_ca.pub

Then, restart sshd:

.. code-block:: bash

    $ systemctl restart sshd

The server is now configured to trust any user certificate signed by `user_ca`.

2. **On the SSH client**:

Configure your SSH client to present your certificate when connecting. The simplest way to do this is to add an IdentityFile line pointing to your private key in your `~/.ssh/config` file:

.. code-block:: bash

    Host *.example-host.com
    IdentityFile ~/path/to/user-key

Now, whenever you connect to an SSH server as a user listed in the certificate (node-user or admin-user in this case), the client will automatically present your user certificate without you needing to specify it on the command line.

Conclusion
----------

You should now be able to SSH into the server using certificate-based authentication. Ensure your certificate is not expired, and if you face any issues, you can debug using:

.. code-block:: bash

    $ ssh -vv [your-server] 2>&1 | grep certificate
