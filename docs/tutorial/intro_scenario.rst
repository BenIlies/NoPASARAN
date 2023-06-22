Introduction to Scenarios
==============================

The JSON file below represents a Finite State Machine (FSM) named `scenario.json`:

.. code-block:: json

   {
     "id": "Tutorial",
     "initial": "First state",
     "states": {
       "First state": {
         "on": {
           "STARTED": {
             "target": "Second State"
           }
         }
       },
       "Second State": {
         "entry": "done",
         "on": {
           "DONE": {
             "target": "Last state"
           }
         }
       },
       "Last state": {}
     }
   }

This JSON file starts with three key-value pairs: `id`, `initial`, and `states`.

- `id`: An identifier for the FSM. In this example, the id is "Tutorial".
- `initial`: Specifies the name of the initial state of the FSM, which is "First state".
- `states`: Contains an object, where each key-value pair represents a state in the FSM.

The `states` object defines three states:

1. `First state`: This is the initial state of the FSM. It includes an `on` key, indicating the possible transitions from this state. In this case, the "STARTED" event causes a transition to the "Second State".

2. `Second State`: This state has an `entry` action named "done", which is performed immediately upon entering the state. The execution of the "done" action inherently triggers the "DONE" event. Once the "DONE" event is triggered, it leads to a transition to the "Last state".

3. `Last state`: This state doesn't define any actions or transitions, implying it is a final state in this FSM.

The FSM operates as follows:

1. The FSM starts in the "First state".
2. When the "STARTED" event is triggered, it transitions to the "Second State".
3. Upon entering the "Second State", the "done" action is executed, which inherently triggers the "DONE" event.
4. As a consequence of the "DONE" event, the FSM transitions to the "Last state".
5. The "Last state" marks the end of this FSM scenario since it does not define any further actions or transitions.

Please note that this is a basic representation of a state machine. In real-world applications, more states, events, and actions would likely be defined to accurately model complex behaviors.
