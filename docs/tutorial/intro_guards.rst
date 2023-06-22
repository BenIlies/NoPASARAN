Introduction to Guards
===============================

This tutorial introduces the concept of guards within a Finite State Machine (FSM). Guards are conditional checks that decide which transition should be taken in a state based on specific conditions associated with an event.

Consider the following JSON representation of our FSM:

.. code-block:: json

   {
     "id": "Tutorial",
     "initial": "Init",
     "states": {
       "Init": {
         "on": {
           "STARTED": {
             "target": "State before guards"
           }
         }
       },
       "State before guards": {
         "entry": [
           "set (true) (value-A)",
           "set (false) (value-B)",
           "done"
         ],
         "on": {
           "DONE": [
             {
               "target": "State not reached",
               "cond": "equal (value-A value-B)"
             },
             {
               "target": "State reached"
             }
           ]
         }
       },
       "State not reached": {},
       "State reached": {}
     }
   }

The JSON file starts with three key-value pairs: `id`, `initial`, and `states`.

- `id`: An identifier for the FSM. In this example, the id is "Tutorial".
- `initial`: Specifies the name of the initial state of the FSM, which in this case is "Init". Note that every FSM will automatically trigger a "STARTED" event when initiated, leading to the execution of the first state.
- `states`: Contains an object, where each key-value pair represents a state in the FSM.

The `states` object defines four states:

1. `Init`: This is the initial state of the FSM. It includes an `on` key, indicating the possible transitions from this state. In this case, the "STARTED" event causes a transition to the "State before guards" state.

2. `State before guards`: This state begins by setting two local variables, "value-A" and "value-B", to `true` and `false` respectively, using the `set` action. After these actions, the "done" action is executed, triggering the "DONE" event. This state includes a guard on the "DONE" event, which checks if "value-A" and "value-B" are equal. If they are, it transitions to the "State not reached". If they are not equal, it transitions to the "State reached" state.

3. `State not reached`: This state is defined but, given the current setup of the FSM, will not be reached since the condition of the guard will always evaluate to false.

4. `State reached`: This state is the final state of the FSM. It doesn't define any actions or transitions, indicating the end of the FSM scenario.

The FSM operates as follows:

1. The FSM is initiated and starts in the "Init" state.
2. Upon initiation, the FSM triggers the "STARTED" event, causing a transition to the "State before guards" state.
3. Upon entering the "State before guards" state, the "set" actions are executed, assigning `true` to "value-A" and `false` to "value-B". After these actions, the "done" action is executed, triggering the "DONE" event.
4. The "DONE" event causes a check of the guard condition. The `equal` primitive compares "value-A" and "value-B". If they were equal, the FSM would transition to the "State not reached" state, but given the values we have set, they are not equal.
5. Because the guard condition is not met, the FSM transitions to the "State reached" state.
6. The "State reached" state is the final state and marks the end of this FSM scenario, as it does not define any further actions or transitions.

This FSM demonstrates the use of guards in state transitions, which are essential for directing the flow of an FSM based on variable conditions.
