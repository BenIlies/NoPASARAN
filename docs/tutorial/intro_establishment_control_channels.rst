Introduction to the Establishment of Control Channels
=====================================================

This tutorial focuses on the establishment of control channels using nested Finite State Machines (FSMs). This nested FSM allows for higher-level abstraction and reusability across different scenarios, similar to traditional programming libraries. 

Here, we will walk through the JSON representation of our main FSM named "MAIN-FSM-CONTROL-CHANNEL" and a nested FSM named "CONTROL-CHANNEL-SET-UP".

**Main FSM: MAIN-FSM-CONTROL-CHANNEL**

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
            "type": "get_parameters (role client server)"
            },
            {
            "type": "done"
            }
        ],
        "on": {
            "DONE": [
            {
                "target": "STARTING CLIENT CONTROL CHANNEL",
                "cond": "equal (role client)"
            },
            {
                "target": "STARTING SERVER CONTROL CHANNEL",
                "cond": "equal (role server)"
            }
            ]
        }
        },
        "STARTING CLIENT CONTROL CHANNEL": {
        "entry": [
            {
            "params": {},
            "type": "load_control_channel_configuration (control_client) (controller_conf)"
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
            "type": "load_control_channel_configuration (control_server) (controller_conf)"
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

**Nested FSM: CONTROL-CHANNEL-SET-UP**

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
                        "type": "get_parameters (role client server)"
                    },
                    {
                        "type": "done"
                    }
                ],
                "on": {
                    "DONE": [
                        {
                            "target": "STARTING CLIENT CONTROL CHANNEL",
                            "cond": "equal (role client)"
                        },
                        {
                            "target": "STARTING SERVER CONTROL CHANNEL",
                            "cond": "equal (role server)"
                        }
                    ]
                }
            },
            "STARTING CLIENT CONTROL CHANNEL": {
                "entry": [
                    {
                        "params": {},
                        "type": "load_control_channel_configuration (control_client) (controller_conf)"
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
                        "type": "load_control_channel_configuration (control_server) (controller_conf)"
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
  

The JSON files starts with three key-value pairs: `id`, `initial`, and `states`.

For the main FSM, the `states` object defines four states:

1. `INIT`: This is the initial state of the FSM. It includes an `on` key, indicating the possible transitions from this state. In this case, the "STARTED" event causes a transition to the "CREATING_CONTROL_CHANNEL" state.

2. `CREATING_CONTROL_CHANNEL`: This state reads the role, client, and server information from the file and sets them up. It then calls the nested FSM, "CONTROL-CHANNEL-SET-UP", with the acquired parameters. After executing the nested FSM, it triggers the returned event, which could be either "CONTROL_CHANNEL_READY" or "TIMEOUT".

3. `SUCCESS ESTABLISHING CONTROL CHANNEL`: This is the final state if the control channel setup is successful. It does not define any further actions or transitions, marking the end of a successful FSM scenario.

4. `TIMEOUT`: This is the final state if a timeout occurs during the control channel setup. It also does not define any further actions or transitions.

The nested FSM, "CONTROL-CHANNEL-SET-UP", establishes a control channel, either as a client or a server, based on the role passed from the main FSM. It includes multiple states from "INITIALIZING" to "CONTROL CHANNEL IS READY", or "TIMEOUT ENDING" in case of a timeout. 

Each of these states performs specific tasks, like loading variables, starting the control channel, and synchronizing the two parties. Depending on the outcome, it either transitions to the "CONTROL CHANNEL IS READY" state, indicating a successful setup, or to the "TIMEOUT ENDING" state, indicating a failure due to timeout.

The FSMs operate as follows:

1. The main FSM, "MAIN-FSM-CONTROL-CHANNEL," is initiated and starts in the "INIT" state.
2. Upon initiation, the main FSM triggers the "STARTED" event, causing a transition to the "CREATING_CONTROL_CHANNEL" state.
3. In the "CREATING_CONTROL_CHANNEL" state of the main FSM, it reads the role, client, and server information from a file and sets them up. It then calls the nested FSM, "CONTROL-CHANNEL-SET-UP," with the acquired parameters.
4. The nested FSM, "CONTROL-CHANNEL-SET-UP," begins in the "INITIALIZING" state upon being called from the main FSM. The "STARTED" event is triggered, leading to a transition to the "LOADING THE VARIABLES" state.
5. In the "LOADING THE VARIABLES" state of the nested FSM, it retrieves the role information (client or server) passed from the main FSM using the get_parameters action. After this, the "done" action is executed, triggering the "DONE" event.
6. The "DONE" event in the nested FSM leads to different transitions based on the role acquired. If the role is "client," it transitions to the "STARTING CLIENT CONTROL CHANNEL" state, and if the role is "server," it transitions to the "STARTING SERVER CONTROL CHANNEL" state.
7. In the "STARTING CLIENT CONTROL CHANNEL" state of the nested FSM, it loads the control channel configuration for the client and configures the client control channel using the load_control_channel_configuration and configure_client_control_channel actions, respectively. Then, it starts the control channel using the start_control_channel action and triggers the "done" event.
8. The "done" event in the "STARTING CLIENT CONTROL CHANNEL" state transitions to the "SYNCHRONIZATION OF THE TWO PARTIES" state in the nested FSM.
9. In the "SYNCHRONIZATION OF THE TWO PARTIES" state, the FSM sets a timeout value of 10 units using the set action. Then, it waits for a ready signal from the control channel, using the wait_ready_signal action with the timeout as a parameter.
10. Depending on whether the ready signal is received before the timeout, the nested FSM either transitions to the "CONTROL CHANNEL IS READY" state or the "TIMEOUT ENDING" state.
11. In the "CONTROL CHANNEL IS READY" state, the nested FSM sets the "CONTROL_CHANNEL_READY" event using the set action and returns the controller_protocol value back to the main FSM using the return_values action.
12. In the "TIMEOUT ENDING" state, the nested FSM sets the "TIMEOUT" event using the set action and returns the controller_protocol value back to the main FSM using the return_values action.


The modular nature of the "CONTROL-CHANNEL-SET-UP" FSM allows it to be reused in various scenarios, highlighting the modularity and reusability of nested FSMs in different contexts.
