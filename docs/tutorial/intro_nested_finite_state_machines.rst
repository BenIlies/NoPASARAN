Introduction to Nested Finite State Machines
============================================

This tutorial introduces the concept of nested Finite State Machines (FSMs). Nested FSMs allow for higher-level abstraction and reusability across different tests, akin to traditional programming libraries. 

Consider the following JSON representation of our main FSM and a nested FSM:

**Main FSM:**

.. code-block:: json

    {
      "id": "MAIN-FSM",
      "initial": "Init",
      "states": {
        "Init": {
          "on": {
            "STARTED": {
              "target": "Intermediate State"
            }
          }
        },
        "Intermediate State": {
          "entry": [
            {
              "type": "set (ping) (input-arg1)"
            },
            {
              "type": "set (pong) (input-arg2)"
            },
            {
              "type": "call (NESTED-FSM input-arg1 input-arg2) (event output-arg1 output-arg2)"
            },
            {
              "type": "trigger (event)"
            }
          ],
          "on": {
            "EVENT_FROM_NESTED_FSM": {
              "target": "End",
              "cond": "equal (input-arg1 output-arg2)",
              "actions": {
                "type": "assign (output-arg1) (output-arg1)"
              }
            }
          }
        },
        "End": {}
      }
    }

**Nested FSM:**

.. code-block:: json

    {
      "id": "NESTED-FSM",
      "initial": "Init",
      "states": {
        "Init": {
          "on": {
            "STARTED": {
              "target": "Catch FSM Input Arguments"
            }
          }
        },
        "Catch FSM Input Arguments": {
          "entry": [
            {
              "type": "get_parameters (fsm-arg1 fsm-arg2)"
            },
            {
              "type": "done"
            }
          ],
          "on": {
            "DONE": {
              "target": "End",
              "actions": [
                {
                  "type": "assign (fsm-arg2) (return-val1)"
                },
                {
                  "type": "assign (fsm-arg1) (return-val2)"
                }
              ]
            }
          }
        },
        "End": {
          "entry": [
            {
              "type": "set (EVENT_FROM_NESTED_FSM) (event)"
            },
            {
              "type": "return_values (event return-val1 return-val2)"
            }
          ]
        }
      }
    }

The JSON file starts with three key-value pairs: `id`, `initial`, and `states`.

- `id`: An identifier for the FSM. In this case, the id is "MAIN-FSM" for the main FSM and "NESTED-FSM" for the nested FSM.
- `initial`: Specifies the name of the initial state of the FSM. Here, the initial state is "Init" for both FSMs. Note that every FSM automatically triggers a "STARTED" event when initiated, leading to the execution of the first state.
- `states`: Contains an object, where each key-value pair represents a state in the FSM.

For the main FSM, the `states` object defines three states:

1. `Init`: This is the initial state of the FSM. It includes an `on` key, indicating the possible transitions from this state. In this case, the "STARTED" event causes a transition to the "Intermediate State".

2. `Intermediate State`: This state sets up two local variables, "input-arg1" and "input-arg2", and assigns them the values "ping" and "pong" respectively using the `set` action. After this, the nested FSM is called using the `call` action. This action requires at least one parameter: the file name of the nested FSM, which, in this case, should be "NESTED-FSM.json", a JSON file located in the current working directory. Additional optional parameters can also be provided to the nested FSM. Following this, the `trigger` action is executed, initiating the nested FSM. The transition from this state depends on the event returned by the nested FSM.

3. `End`: This is the final state of the main FSM. It does not define any further actions or transitions, marking the end of the FSM test.

The nested FSM, similar to the main FSM, begins in the "Init" state. On receiving the "STARTED" event, it transitions to the "Catch FSM Input Arguments" state. Here, it retrieves the input arguments passed from the main FSM using the `get_parameters` primitive. Following this, the "DONE" event leads to a transition to the "End" state. The "End" state sets an event identifier and returns the required values back to the main FSM using the `return_values` action.

The FSMs operate as follows:

1. The main FSM is initiated and starts in the "Init" state.
2. Upon initiation, the main FSM triggers the "STARTED" event, causing a transition to the "Intermediate State".
3. Upon entering the "Intermediate State", the `set` actions are executed, assigning "ping" to "input-arg1" and "pong" to "input-arg2". The `call` action is then executed, calling the nested FSM and passing in the arguments "input-arg1" and "input-arg2".
4. The nested FSM begins in the "Init" state. The "STARTED" event is triggered, leading to a transition to the "Catch FSM Input Arguments" state.
5. The nested FSM retrieves the input arguments using the `get_parameters` action and then executes the "done" action, triggering the "DONE" event.
6. The "DONE" event in the nested FSM triggers the transition to the "End" state. In this state, an event identifier is set, and the `return_values` action passes the return values back to the main FSM.
7. In the main FSM, the returned event from the nested FSM is detected, triggering the "EVENT_FROM_NESTED_FSM" transition. The `equal` condition is checked, and if it holds true (which it should, since "input-arg1" ("ping") is equal to "output-arg2" ("ping")), the FSM transitions to the "End" state. The `assign` action is then executed, storing "output-arg1" in the final state.
8. The "End" state is the final state and marks the end of this FSM test as it does not define any further actions or transitions.

At the end of this process, "output-arg1", which was returned by the nested FSM and assigned to "output-arg1" in the main FSM, should hold the value "pong". This demonstrates the transfer of data between nested FSMs.
