from nopasaran.decorators import parsing_decorator
import psutil
import logging

class SocketPrimitives:
    """
    Class containing Socket action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def free_socket(inputs, outputs, state_machine):
        """
        Kill the process using a specific port, thus freeing the socket.

        Number of input arguments: 1

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the port number.

            outputs (List[str]): There are no output arguments.

            state_machine: The state machine object.

        Returns:
            None
        """
        port = int(state_machine.get_variable_value(inputs[0]))

        # Find the process using the port
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == port:
                process = psutil.Process(conn.pid)
                try:
                    # Kill the process holding the port
                    process.terminate()
                    process.wait(timeout=0.5)  # Wait for the process to terminate
                    logging.info(f"[Socket] Process {conn.pid} using port {port} has been terminated.")
                    return
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
                    logging.error(f"[Socket] Failed to terminate process {conn.pid} using port {port}: {e}")
                    return

        logging.info(f"[Socket] No process found using port {port}, nothing to free.")
