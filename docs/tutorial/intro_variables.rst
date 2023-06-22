Introduction to Variables
==================================

This tutorial focuses on introducing the concept of local variables within states in a Finite State Machine (FSM), and how values can be assigned from one state to another. It demonstrates the use of the `get_from_file` primitive, which takes two arguments: a JSON file name, and the name of a variable within that file. The output of this primitive is then assigned to a local variable within a state. Similarly, the `assign` primitive is used to assign variables between states.

Here's the JSON file that represents our FSM:

.. code-block:: json

   {
     "id": "Tutorial",
     "initial": "Init",
     "states": {
       "Init": {
         "on": {
           "STARTED": {
             "target": "Variables Creation"
           }
         }
       },
       "Variables Creation": {
         "entry": [
           "get_from_file (variables ip-server) (ip-old-state)",
           "get_from_file (variables port-server) (port-old-state)",
           "done"
         ],
         "on": {
           "DONE": {
             "target": "Variables Reception",
             "actions": [
               "assign (ip-old-state) (ip-new-state)",
               "assign (port-old-state) (port-new-state)"
             ]
           }
         }
       },
       "End": {},
       "Variables Reception": {
         "entry": "done",
         "on": {
           "DONE": {
             "target": "End"
           }
         }
       }
     }
   }

The JSON file starts with three key-value pairs: `id`, `initial`, and `states`.

- `id`: An identifier for the FSM. In this example, the id is "Tutorial".
- `initial`: Specifies the name of the initial state of the FSM, which is "Init". Note that every FSM will automatically trigger a "STARTED" event when initiated.
- `states`: Contains an object, where each key-value pair represents a state in the FSM.

The `states` object defines four states:

1. `Init`: This is the initial state of the FSM. It includes an `on` key, indicating the possible transitions from this state. In this case, the "STARTED" event causes a transition to the "Variables Creation" state.

2. `Variables Creation`: Upon entering this state, two `get_from_file` actions are executed. These actions retrieve the specified variables ("ip-server" and "port-server") from the specified file ("variables.json") and assign them to local variables ("ip-old-state" and "port-old-state"). Once these actions have been executed, the "done" action triggers the "DONE" event, leading to a transition to the "Variables Reception" state. As part of this transition, the `assign` actions are executed, which assign the values of "ip-old-state" and "port-old-state" to new state variables ("ip-new-state" and "port-new-state").

3. `Variables Reception`: This state is responsible for receiving and storing the values assigned from the "Variables Creation" state. Upon entering this state, the "done" action is executed, which inherently triggers the "DONE" event, leading to a transition to the `End` state.

4. `End`: This state is the final state and marks the completion of the FSM, as it does not define any further actions or transitions.

The FSM operates as follows:

1. The FSM starts in the "Init" state.
2. When the "STARTED" event is triggered, it transitions to the "Variables Creation" state.
3. Upon entering the "Variables Creation" state, the FSM executes the `get_from_file` actions, retrieving the values of the specified variables from the given file and assigning them to local state variables. After these actions, the "done" action is executed, triggering the "DONE" event.
4. As a consequence of the "DONE" event, the FSM transitions to the "Variables Reception" state. During this transition, the values of the local variables in the previous state are assigned to new state variables.
5. Upon entering the "Variables Reception" state, the "done" action is executed again, triggering another "DONE" event, leading the FSM to transition to the "End" state.
6. The "End" state is the final state and marks the end of this FSM scenario, as it does not define any further actions or transitions.

This FSM illustrates the concept of creating, assigning, and transferring local state variables using the `get_from_file` and `assign` primitives. It shows how state machines can manipulate and pass data between states, an essential aspect of state machine functionality in complex systems.
