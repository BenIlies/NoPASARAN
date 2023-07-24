Introduction to Sync Messages
=============================

This tutorial focuses on exchanging sync messages using a nested Finite State Machine (FSM) named "EXCHANGE-SYNC." The FSM demonstrates how to synchronize with the remote endpoint using the control channel. The synchronization process involves sending and receiving fixed strings and random integers between two parties, waiting for synchronization, and handling timeouts.

**Nested FSM: EXCHANGE-SYNC**

Below is the JSON representation of the nested FSM named "EXCHANGE-SYNC":

.. code-block:: json

    {
        "id": "EXCHANGE-SYNC",
        "initial": "INITIALIZING",
        "states": {
            "INITIALIZING": {
                "on": {
                    "STARTED": {
                        "target": "LOADING_PARAMETERS"
                    }
                }
            },
            "LOADING_PARAMETERS": {
                "entry": [
                    {
                        "params": {},
                        "type": "get_parameters (ctrl)"
                    },
                    {
                        "params": {},
                        "type": "done"
                    }
                ],
                "on": {
                    "DONE": {
                        "target": "Second State",
                        "actions": {
                            "params": {},
                            "type": "assign (ctrl) (ctrl)"
                        }
                    }
                }
            },
            "Second State": {
                "entry": [
                    {
                        "params": {},
                        "type": "set (hello_from_remote_endpoint) (fixed_string_to_sync)"
                    },
                    {
                        "params": {},
                        "type": "set_random_int(1 2) (random_integer_to_sync)"
                    },
                    {
                        "params": {},
                        "type": "sync (ctrl fixed_string_to_sync random_integer_to_sync)"
                    }
                ],
                "on": {
                    "SYNC_SENT": {
                        "target": "new state 2",
                        "actions": {
                            "params": {},
                            "type": "assign (ctrl) (ctrl)"
                        }
                    }
                }
            },
            "new state 2": {
                "entry": [
                    {
                        "params": {},
                        "type": "set (5) (timeout)"
                    },
                    {
                        "params": {},
                        "type": "set_integer (2) (even_number)"
                    },
                    {
                        "params": {},
                        "type": "wait_sync_signal (ctrl timeout) (fixed_string_received random_integer_received)"
                    }
                ],
                "on": {
                    "TIMEOUT": {
                        "target": "TIMEOUT"
                    },
                    "SYNC_AVAILABLE": [
                        {
                            "target": "EVEN NUMBER RECEIVED FROM REMOTE",
                            "cond": "equal (even_number random_integer_received)"
                        },
                        {
                            "target": "ODD NUMBER RECEIVED FROM REMOTE"
                        }
                    ]
                }
            },
            "TIMEOUT": {
                "entry": [
                    {
                        "params": {},
                        "type": "set (TIMEOUT) (event)"
                    },
                    {
                        "params": {},
                        "type": "return_values (event)"
                    }
                ]
            },
            "EVEN NUMBER RECEIVED FROM REMOTE": {
                "entry": [
                    {
                        "params": {},
                        "type": "set (SYNC_SUCCESS_WITH_EVEN) (event)"
                    },
                    {
                        "params": {},
                        "type": "return_values (event)"
                    }
                ]
            },
            "ODD NUMBER RECEIVED FROM REMOTE": {
                "entry": [
                    {
                        "type": "set (SYNC_SUCCESS_WITH_ODD) (event)"
                    },
                    {
                        "type": "return_values (event)"
                    }
                ]
            }
        }
    }

**Operation of the FSM**

1. **Initialization:** The FSM starts in the "INITIALIZING" state, awaiting the "STARTED" event to be triggered.

2. **Loading Parameters:** In the "LOADING PARAMETERS" state, the FSM fetches the "ctrl" parameter from the environment using the "get_parameters" action and assigns it to the "ctrl" variable. It then proceeds to the next state.

3. **Sending Messages Synchronization:** In the "SEND MESSAGES SYNCHRONIZATION" state, the FSM sets a fixed string "hello_from_remote_endpoint" and a random integer "random_integer_to_sync." It then initiates synchronization by using the "sync" action with the provided parameters.

4. **Wait for Synchronization:** The FSM transitions to the "WAIT FOR SYNCHRONIZATION" state after sending the sync messages. In this state, it sets a timeout value of 5 seconds and assigns the even number "2" to the "even_number" variable. It then waits for a sync signal using the "wait_sync_signal" action, which receives the "ctrl," "timeout," "fixed_string_received," and "random_integer_received" as parameters.

5. **Timeout Handling:** If the FSM receives no sync signal before the timeout, it transitions to the "TIMEOUT" state.

6. **Synchronization Success:** If the FSM receives a sync signal before the timeout, it checks whether the "random_integer_received" is even or odd. If it is even, the FSM transitions to the "EVEN NUMBER RECEIVED FROM REMOTE" state; otherwise, it transitions to the "ODD NUMBER RECEIVED FROM REMOTE" state.

7. **Even Number Received from Remote:** In the "EVEN NUMBER RECEIVED FROM REMOTE" state, the FSM sets the "SYNC_SUCCESS_WITH_EVEN" event and returns the values.

8. **Odd Number Received from Remote:** In the "ODD NUMBER RECEIVED FROM REMOTE" state, the FSM sets the "SYNC_SUCCESS_WITH_ODD" event and returns the values.

**Conclusion**

In this tutorial, we delved into the inner workings of the "EXCHANGE-SYNC" nested Finite State Machine, which showcases the process of exchanging sync messages using a control channel. Through this FSM, we learned how to synchronize two parties by sending and receiving fixed strings and random integers, while also handling timeouts effectively.

**Additional Information**

- The "sync" action and "wait_sync_signal" action may take more or fewer values, but the number of output variables in the "wait_sync_signal" action should match the number of input variables minus 1 in the "sync" action.
- The values sent in sync messages can be of any object type based on the requirements of the communication.
