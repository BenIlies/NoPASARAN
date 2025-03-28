Configuring Worker Using Existing NoPASARAN Coordinator
=======================================================

1. Visit the Docker Documentation
---------------------------------
Go to the official Docker documentation for reference:

   https://docs.docker.com/

2. Add Docker's Official GPG Key
--------------------------------
Below is an example for **Ubuntu**. Adjust commands as necessary for your specific operating system.

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

Add the Docker repository to your system’s Apt sources:

.. code-block:: bash

   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
     $(. /etc/os-release && echo \"${UBUNTU_CODENAME:-$VERSION_CODENAME}\") stable" | \
     sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

   sudo apt-get update

3. Save & Execute the Docker Installation Script
------------------------------------------------
Create or save a script with the commands from the previous step, then run it. For example:

.. code-block:: bash

   # Paste the commands from above into shell.sh, then save and exit.
   nano shell.sh

   bash shell.sh

4. Install Docker Packages
--------------------------
Run the following command to install Docker and related components:

.. code-block:: bash

   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

5. Log in to a Coordinator
--------------------------

Go to your coordinator (below we assume that we use the official one):

`NoPASARAN Coordinator <https://www.nopasaran.org/>`_

Enter your credentials to access your NoPASARAN dashboard.

6. Identify Your Target Worker
-----------------------------
- Find the **name** of the worker that you want to configure your device to use.

7. Open the Worker Settings
---------------------------
- Click the **Settings** icon for your chosen worker (hover over it to see **Configure endpoint**).

8. Copy the Configuration
-------------------------
- Press the **Copy configuration** button to copy the Docker configuration details.

9. Navigate to Your Downloads Folder
------------------------------------
- Switch to your **Downloads** directory .

10. Create a Docker Compose File
-------------------------------
Create a file named **docker-compose.yml**:

.. code-block:: bash

   nano docker-compose.yml

Paste the copied configuration into this file.

11. Install Docker Compose (If Not Already Installed)
----------------------------------------------------
If Docker Compose is not already installed, you can do so with:

.. code-block:: bash

   sudo apt install docker-compose

12. Add Your User to the Docker Group
-------------------------------------
Give your user permissions to run Docker commands without using **sudo** each time:

.. code-block:: bash

   sudo usermod -aG docker $(whoami)

13. Reboot the Device
---------------------
Reboot your system to apply group membership changes:

.. code-block:: bash

   sudo reboot

14. Start the Docker Compose Service
------------------------------------
After the reboot, return to your **Downloads** folder (or wherever **docker-compose.yml** is saved) and run:

.. code-block:: bash

   docker-compose up
