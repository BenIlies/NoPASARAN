import json
import time

from twisted.internet.threads import deferToThread

from nopasaran.controllers.controller import ClientController, ServerController
from nopasaran.definitions.control_channel import JSONMessage, Status, Configuration
from nopasaran.definitions.events import EventNames
from nopasaran.decorators import parsing_decorator


class ControlChannelPrimitives:
    """
    Class containing control channel action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def load_control_channel_configuration(inputs, outputs, state_machine):
        """
        Load the control channel configuration from a file and store it in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the file path, and one mandatory output argument, which is the name of the variable to store the loaded configuration.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable where the loaded configuration will be stored.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        controller_configuration = json.load(open('.'.join((inputs[0], 'json'))))
        state_machine.set_variable_value(outputs[0], controller_configuration)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=2)
    def configure_client_control_channel(inputs, outputs, state_machine):
        """
        Configure the client control channel using the controller configuration from the machine's state.

        Number of input arguments: 1

        Number of output arguments: 2

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable storing the configuration, and two mandatory output arguments, which are the names of the variables where the configured controller and controller protocols will be stored.
            
            outputs (List[str]): The list of output variable names. It contains two mandatory output arguments, which are the names of the variables where the configured controller and controller protocols will be stored.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        controller_configuration = state_machine.get_variable_value(inputs[0])
        state_machine.set_variable_value(outputs[1], None)
        controller = ClientController(state_machine, outputs[1], controller_configuration[Configuration.ROOT_CERTIFICATE.name], controller_configuration[Configuration.PRIVATE_CERTIFICATE.name])
        controller.configure(controller_configuration[Configuration.DESTINATION_IP.name], int(controller_configuration[Configuration.SERVER_PORT.name]))
        state_machine.set_variable_value(outputs[0], controller)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=2)
    def configure_server_control_channel(inputs, outputs, state_machine):
        """
        Configure the server control channel using the controller configuration from the machine's state.

        Number of input arguments: 1

        Number of output arguments: 2

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable storing the configuration, and two mandatory output arguments, which are the names of the variables where the configured controller and controller protocols will be stored.
            
            outputs (List[str]): The list of output variable names. It contains two mandatory output arguments, which are the names of the variables where the configured controller and controller protocols will be stored.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        controller_configuration = state_machine.get_variable_value(inputs[0])
        state_machine.set_variable_value(outputs[1], None)
        controller = ServerController(state_machine, outputs[1], controller_configuration[Configuration.ROOT_CERTIFICATE.name], controller_configuration[Configuration.PRIVATE_CERTIFICATE.name])
        controller.configure(int(controller_configuration[Configuration.SERVER_PORT.name]))
        state_machine.set_variable_value(outputs[0], controller)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def start_control_channel(inputs, outputs, state_machine):
        """
        Start the control channel using the specified variable's value from the machine's state.

        Number of input arguments: 1

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable storing the control channel object.
            
            outputs (List[str]): The list of output variable names.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        deferToThread(state_machine.get_variable_value(inputs[0]).start)


    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def wait_ready_signal(inputs, outputs, state_machine):
        """
        Wait for the local and remote status of the controller protocol to be READY.
        If the status becomes READY within the specified timeout (input argument),
        triggers the event READY. Otherwise, triggers the event TIMEOUT.

        Number of input arguments: 2

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the names of the local and remote status variables, and the timeout value.
            
            outputs (List[str]): The list of output variable names.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        timeout = False
        start_time = time.time()
        while True:
            controller_protocol = state_machine.get_variable_value(inputs[0])
            if controller_protocol:
                if controller_protocol.local_status == Status.READY.name and controller_protocol.remote_status == Status.READY.name:
                    break
            if time.time() - start_time > float(state_machine.get_variable_value(inputs[1])):
                timeout = True
                break
        if timeout:
            state_machine.trigger_event(EventNames.TIMEOUT.name)
        else:
            state_machine.trigger_event(EventNames.READY.name)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0, optional_inputs=True)
    def sync(inputs, outputs, state_machine):
        """
        Send a synchronization message containing the provided inputs to the controller protocol.
        Triggers the event SYNC_SENT.

        Number of input arguments: 1

        Number of output arguments: 0

        Optional input arguments: Yes

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable storing the inputs to be synchronized, and optional input arguments representing additional synchronization inputs.
            
            outputs (List[str]): The list of output variable names.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        controller_protocol = state_machine.get_variable_value(inputs[0])
        if controller_protocol:
            data_to_send = [state_machine.get_variable_value(input_value) for input_value in inputs[1:]]
            controller_protocol.send_sync(data_to_send)
            state_machine.trigger_event(EventNames.SYNC_SENT.name)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0, optional_outputs=True)
    def wait_sync_signal(inputs, outputs, state_machine):
        """
        Wait for a synchronization message to be available in the controller protocol's queue.
        If a message becomes available within the specified timeout (input argument),
        store its contents in the output variables and trigger the event SYNC_AVAILABLE.
        Otherwise, triggers the event TIMEOUT.

        Number of input arguments: 2

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: Yes

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the name of the variable storing the received synchronization message, and the timeout value.
            
            outputs (List[str]): The list of output variable names. It contains the names of the variables where the synchronization message will be stored (optional).
            
            state_machine: The state machine object.

        Returns:
            None
        """
        timeout = False
        start_time = time.time()
        sync_message = None
        while True:
            controller_protocol = state_machine.get_variable_value(inputs[0])
            if controller_protocol:
                if len(controller_protocol.queue) > 0:
                    sync_message = controller_protocol.queue[0]
                    controller_protocol.queue.pop(0)
                    break
            if time.time() - start_time > float(state_machine.get_variable_value(inputs[1])):
                timeout = True
                break
        if timeout:
            state_machine.trigger_event(EventNames.TIMEOUT.name)
        else:
            for index in range(len(outputs)):
                state_machine.set_variable_value(outputs[index], sync_message[index])
            state_machine.trigger_event(EventNames.SYNC_AVAILABLE.name)