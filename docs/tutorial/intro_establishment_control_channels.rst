Introduction to the Establishment of Control Channels
=====================================================

This tutorial focuses on the establishment of control channels using a nested Finite State Machine (FSM). The nested FSM presented here allows for higher-level abstraction and reusability across different scenarios. It serves as a practical implementation to facilitate the establishment of control channels, be it as a client or as a server.

**Nested FSM: CONTROL-CHANNEL-SET-UP**

Below is the JSON representation of the nested FSM named "CONTROL-CHANNEL-SET-UP." It is designed to establish control channels, either as a client or as a server, based on the role passed from the environment. This FSM requires two mandatory input variables, "role" and "controller_conf_filename."

.. code-block:: json

    {
        "id": "CONTROL-CHANNEL-SET-UP",
        "initial": "INITIALIZING",
        "states": {
            "INITIALIZING": {
                "on": {
                    "STARTED": {
                        "target": "LOADING THE VARIABLES"
                    }
                }
            },
            "LOADING THE VARIABLES": {
                "entry": [
                    {
                        "params": {},
                        "type": "get_parameters (role controller_conf_filename)"
                    },
                    {
                        "params": {},
                        "type": "set (client) (client)"
                    },
                    {
                        "type": "set (server) (server)"
                    },
                    {
                        "type": "done"
                    }
                ],
                "on": {
                    "DONE": [
                        {
                            "target": "STARTING CLIENT CONTROL CHANNEL",
                            "cond": "equal (role client)",
                            "actions": {
                                "type": "assign (controller_conf_filename) (controller_conf_filename)"
                            }
                        },
                        {
                            "target": "STARTING SERVER CONTROL CHANNEL",
                            "cond": "equal (role server)",
                            "actions": {
                                "type": "assign (controller_conf_filename) (controller_conf_filename)"
                            }
                        }
                    ]
                }
            },
            "STARTING CLIENT CONTROL CHANNEL": {
                "entry": [
                    {
                        "params": {},
                        "type": "load_control_channel_configuration (controller_conf_filename) (controller_conf)"
                    },
                    {
                        "params": {},
                        "type": "configure_client_control_channel (controller_conf) (controller controller_protocol)"
                    },
                    {
                        "params": {},
                        "type": "start_control_channel (controller)"
                    },
                    {
                        "params": {},
                        "type": "done"
                    }
                ],
                "on": {
                    "DONE": {
                        "target": "SYNCHRONIZATION OF THE TWO PARTIES",
                        "actions": {
                            "params": {},
                            "type": "assign (controller_protocol) (controller_protocol)"
                        }
                    }
                }
            },
            "STARTING SERVER CONTROL CHANNEL": {
                "entry": [
                    {
                        "params": {},
                        "type": "load_control_channel_configuration (controller_conf_filename) (controller_conf)"
                    },
                    {
                        "params": {},
                        "type": "configure_server_control_channel (controller_conf) (controller controller_protocol)"
                    },
                    {
                        "params": {},
                        "type": "start_control_channel (controller)"
                    },
                    {
                        "params": {},
                        "type": "done"
                    }
                ],
                "on": {
                    "DONE": {
                        "target": "SYNCHRONIZATION OF THE TWO PARTIES",
                        "actions": {
                            "params": {},
                            "type": "assign (controller_protocol) (controller_protocol)"
                        }
                    }
                }
            },
            "SYNCHRONIZATION OF THE TWO PARTIES": {
                "entry": [
                    {
                        "params": {},
                        "type": "set (10) (timeout)"
                    },
                    {
                        "params": {},
                        "type": "wait_ready_signal (controller_protocol timeout)"
                    }
                ],
                "on": {
                    "TIMEOUT": {
                        "target": "TIMEOUT ENDING",
                        "actions": {
                            "params": {},
                            "type": "assign (controller_protocol) (controller_protocol)"
                        }
                    },
                    "READY": {
                        "target": "CONTROL CHANNEL IS READY",
                        "actions": {
                            "params": {},
                            "type": "assign (controller_protocol) (controller_protocol)"
                        }
                    }
                }
            },
            "TIMEOUT ENDING": {
                "entry": [
                    {
                        "params": {},
                        "type": "set (TIMEOUT) (event)"
                    },
                    {
                        "params": {},
                        "type": "return_values (event controller_protocol)"
                    }
                ]
            },
            "CONTROL CHANNEL IS READY": {
                "entry": [
                    {
                        "params": {},
                        "type": "set (CONTROL_CHANNEL_READY) (event)"
                    },
                    {
                        "params": {},
                        "type": "return_values (event controller_protocol)"
                    }
                ]
            }
        }
    }

**Input Variables**

The "CONTROL-CHANNEL-SET-UP" FSM expects the following input variables:

1. "role": Specifies the role of the control channel, which can be either "client" or "server".

2. "controller_conf_filename": The filename containing the configuration settings required for establishing the control channel.

**Output Variables**

The "CONTROL-CHANNEL-SET-UP" FSM can produce different output variables based on its ending:

1. If the FSM ends successfully after establishing the control channel, it triggers the "CONTROL_CHANNEL_READY" event and provides the "controller_channel" variable to be used for successful communication.

2. If the FSM ends with a timeout before the control channel is established, it triggers the "TIMEOUT" event and still returns the "controller_channel" that was attempted for the establishment.

**Operation of the FSM**

The "CONTROL-CHANNEL-SET-UP" FSM operates as follows:

1. **Initialization**: The FSM starts in the "INITIALIZING" state, awaiting the "STARTED" event to be triggered.

2. **Loading Variables**: In the "LOADING THE VARIABLES" state, the FSM fetches the "role" and "controller_conf_filename" from the environment using the "get_parameters" action. It then sets "client" to the "client" variable and "server" to the "server" variable using the "set" action.

3. **Starting Control Channel**: Based on the acquired role, the FSM transitions either to the "STARTING CLIENT CONTROL CHANNEL" or the "STARTING SERVER CONTROL CHANNEL" state. The transitions are determined by "cond" conditions based on the role, and the FSM stores the "controller_conf_filename" using the "assign" action before transitioning.

4. **Client Control Channel Setup**: In the "STARTING CLIENT CONTROL CHANNEL" state, the FSM loads the control channel configuration for the client using the "load_control_channel_configuration" action with "controller_conf_filename" as a parameter. It then configures the client control channel and starts it using appropriate actions. Upon successful completion, the FSM triggers the "DONE" event, leading to the "SYNCHRONIZATION OF THE TWO PARTIES" state.

5. **Server Control Channel Setup**: Similarly, in the "STARTING SERVER CONTROL CHANNEL" state, the FSM loads the control channel configuration for the server and performs the necessary setup actions before transitioning to the "SYNCHRONIZATION OF THE TWO PARTIES" state.

6. **Synchronization**: In the "SYNCHRONIZATION OF THE TWO PARTIES" state, the FSM sets a timeout value of 10 seconds using the "set" action and waits for a ready signal from the control channel. If the ready signal is received before the timeout, it transitions to the "CONTROL CHANNEL IS READY" state; otherwise, it transitions to the "TIMEOUT ENDING" state.

7. **Timeout Handling**: In the "TIMEOUT ENDING" state, the FSM sets the "TIMEOUT" event and still returns the "controller_channel" that was attempted for the establishment.

8. **Control Channel Ready**: In the "CONTROL CHANNEL IS READY" state, the FSM triggers the "CONTROL_CHANNEL_READY" event and provides the "controller_channel" value.

**Conclusion**

In this tutorial, we have explored the practical implementation of a nested Finite State Machine, the "CONTROL-CHANNEL-SET-UP," designed to establish control channels as a client or as a server. The FSM provides a higher level of abstraction and reusability, making it an efficient solution for control channel setup in various scenarios.