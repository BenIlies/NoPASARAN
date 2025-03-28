Tests and Tests-Trees: Deployment Guide
=======================================

1. Fork & Clone the Main Repository (Tests Library)
---------------------------------------------------
**Fork** the main repository to your GitHub account:

   `https://github.com/nopasaran-org/nopasaran-tests`

**Clone** your forked repository locally:

.. code-block:: bash
   
   git clone https://github.com/your-username/nopasaran-tests.git

2. Add State Machine Directories & JSON Configurations
------------------------------------------------------

In your forked **nopasaran-tests** repository, create a directory (e.g., **NAT_TRANSLATION**). Conventionally, test directories should be named in uppercase.

This directory must contain the required JSON configuration files, including:

   - **MAIN.json** (entry point)
   - **SERVER_SIGNALLING.json**
   - **CONTROL_CHANNEL_SET_UP.json**
   - **EXCHANGE_SYNC.json**

3. Save, Push, and Create a Pull Request
-------------------------------------------

Follow these steps to save and submit your changes:

**Stage your files**:

.. code-block:: bash
   
   git add NAT_TRANSLATION

**Commit your changes**:

.. code-block:: bash
   
   git commit -m "Added NAT_TRANSLATION test"

**Push to your fork**:

.. code-block:: bash
   
   git push origin main

**Create a Pull Request**:
   - Navigate to your fork on GitHub.
   - Click **Compare & pull request**.
   - Ensure the changes are correct, then submit the request.

4. Fork & Clone the Main Repository (Tests-Trees Library)
-------------------------------------------------------------

**Fork** the main repository to your GitHub account:

   `https://github.com/nopasaran-org/nopasaran-tests-trees`

**Clone** your forked repository locally:

.. code-block:: bash
   
   git clone https://github.com/your-username/nopasaran-tests-trees.git

5. Modify `tests_tree.py`
----------------------------

In the **nopasaran-tests-trees** repository, locate and open `example/tests_tree.py`. This file contains a sample tests-tree. You can copy this file to the root folder and modify it to create a tests-tree that uses the **NAT_TRANSLATION** test with a single node in the tree.

**Remove the following line (if present)**:

.. code-block:: python
   
   TestsTreeTest.load_and_evaluate_tree()

**Delete child workers**:
   Remove them from both `load_and_evaluate_tree()` and `save_tree()`.

**Update PNG image filename**:
   Modify the name of the generated image file to `nat_debugger.png`. Unlike test directories, tests-trees use lowercase naming conventions.

6. Update the `save_tree()` Method
-------------------------------------

Modify the `save_tree()` function in `tests_tree.py` to include appropriate inputs:

.. code-block:: python
   
   def save_tree():
       root = TestsTreeNode(
           'Root',
           num_workers=2,
           inputs=[
               {
                   'role': ("client", True),
                   'client': ("client", True),
                   'server': ("server", True),
                   'ip': (None, False),
                   'port': (None, False)
               },
               {
                   'role': ("server", True),
                   'client': ("client", True),
                   'server': ("server", True),
                   'filter': (None, False)
               }
           ],
           test='NAT_TRANSLATION'
       )

**Match Test Names**
Ensure the test name in your node matches the folder name created in the **nopasaran-tests** repository, in this case, **NAT_TRANSLATION**.

**Note:**
   - `("name", Boolean)` determines if a variable has a default value.
   - `(None, False)` means the variable has no default value.

7. Run the Code
------------------

**Install dependencies**:

.. code-block:: bash
   
   python -m pip install -r requirements.txt

**Generate the image**:

.. code-block:: bash
   
   python example.py

8. Generate & Handle the PNG Image
-------------------------------------

When the tests-tree is generated, a PNG image (`nat_debugger.png`) may be created in **nopasaran-tests-trees**.

**Ensure** that the PNG file is located in the **root folder** of your **nopasaran-tests** fork.

**Stage the file**:

.. code-block:: bash
   
   git add nat_debugger.png

**Do not push** modifications to `tests_tree.py` back to **nopasaran-tests-trees**; only push the **new image** to your **nopasaran-tests** fork.

9. Prepare & Submit a Pull Request
-------------------------------------

**Commit the new image**:

.. code-block:: bash
   
   git commit -m "Added nat_debugger.png"

**Push changes**:

.. code-block:: bash
   
   git push origin main

**Open a Pull Request**:
   - Navigate to your fork on GitHub.
   - Click **Compare & pull request**.
   - Submit the request to **nopasaran-tests**.

.. note::
   Ensure all references—such as roles, test names, image names, JSON files, and worker configurations—are consistent with your updated code and repository structure.
