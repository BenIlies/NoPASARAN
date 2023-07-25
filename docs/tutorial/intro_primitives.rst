Introduction to Primitives
==========================

Primitives are fundamental, hardcoded functions that execute specific operations within our system. These actions range from creating variables and sending packets to calling state machines and returning results to parent state machines.

Primitives play a crucial role in executing actions, and their structure follows a specific pattern:

::

    primitive-name (input-argument-1 input-argument-2) (output-argument-1 output-argument-2 output-argument-3)

In this documentation, we'll explore the characteristics of primitives and their usage in detail.

Structure of Primitives
-----------------------

Primitives consist of the following components:

1. **Primitive Name:** This identifies the specific operation the primitive performs.

2. **Input Arguments:** These are the values required as input for the primitive to execute.

3. **Output Arguments:** These are the results or values returned by the primitive.

Primitives are organized using spaces and enclosed in parentheses, with input and output arguments separated by spaces.

Mandatory Inputs and Outputs
----------------------------

One essential feature of primitives is that they have a fixed number of mandatory inputs and outputs. For instance, consider the "set" primitive, which requires one mandatory input and one mandatory output. It takes a string as input and stores it in a variable, with the variable name provided as the output. Here's an example:

::

    "set (string) (variable_name)"

In Python, this would be equivalent to:

::

    variable_name = "string"

Primitives without Parentheses
------------------------------

Some primitives, like "done," trigger events without any input or output argument. These primitives do not require parentheses and are straightforward in their execution.

Primitives with Single Parentheses
----------------------------------

Certain primitives, like "send" and "create_UDP_packet," have only one set of parentheses. However, they differ in functionality. The "send" primitive sends a packet from a stored variable (input), while the "create_UDP_packet" primitive creates a variable and stores it inside another variable (output).

Primitives with Optional Inputs and Outputs
-------------------------------------------

Some primitives may have optional input and output arguments. For instance, the "call" primitive is used to invoke nested state machines. The API reference may mention one mandatory input argument and zero mandatory output arguments. However, the "call" function can accept multiple input and output arguments as necessary. For example:

::

    call (NESTED-STATE-MACHINE input-variable-1 input-variable-2 input-variable-3) (output-variable-1)

Refer to the documentation for specific requirements of nested state machines.

Conclusion
----------

In this documentation, we've covered the structure and usage of primitives in our system. Primitives are vital for executing actions and ensuring smooth operations within our framework. Detailed descriptions of each primitive can be found in the API Reference section, offering valuable insights into their functionalities and proper usage.

By following this guide, you'll have a better understanding of primitives and their significance in our system's workflow.
