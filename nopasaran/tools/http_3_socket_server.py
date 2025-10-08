import asyncio
import logging
import ssl
from typing import Dict, Any
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.h3.connection import H3Connection
from aioquic.h3.events import HeadersReceived, DataReceived
from nopasaran.definitions.events import EventNames
from nopasaran.http_3_utils import create_quic_configuration
from nopasaran.tools.http_3_socket_base import HTTP3SocketBase
import nopasaran.tools.http_3_overwrite

logger = logging.getLogger("http3_server")


class HTTP3SocketServer(HTTP3SocketBase):
    """HTTP/3 server implementation with deterministic frame injection support"""
    
    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.server = None
        self.client_connections = {}  # Track client connections

    async def start(self):
        """Start the HTTP/3 server"""
        try:
            # Create QUIC configuration (TLS always enabled for HTTP/3)
            configuration = create_quic_configuration(
                is_client=False
            )
            
            # Create server protocol factory
            def create_protocol():
                protocol = QuicConnectionProtocol(configuration)
                connection = H3Connection(protocol._quic)
                
                # Store this connection for later use
                self.protocol = protocol
                self.connection = connection
                
                return protocol
            
            # Start the server
            self.server = await serve(
                self.host,
                self.port,
                configuration=configuration,
                create_protocol=create_protocol
            )
            
            return EventNames.SERVER_STARTED.name, f"Server successfully started at {self.host}:{self.port} with TLS."
            
        except Exception as e:
            return EventNames.ERROR.name, f"Failed to start server: {str(e)}"

    async def run_communication(self, frame_spec: Dict[str, Any] = None):
        """
        Run server-side HTTP/3 communication with optional deterministic frame injection.
        
        Args:
            frame_spec: Dictionary containing client_frames and server_frames to inject
        """
        if frame_spec:
            self.set_deterministic_frames(frame_spec)
        
        try:
            # Wait for client connection and handle communication
            while True:
                # Receive events from clients
                events = await self._receive_frame(timeout=1.0)
                
                if events:
                    for event in events:
                        await self._handle_server_event(event)
                
                # Send deterministic server frames if configured
                if self.deterministic_frames and "server_frames" in self.deterministic_frames:
                    await self.send_deterministic_frames("server_frames")
                
                await asyncio.sleep(0.01)
                
        except Exception as e:
            logger.error(f"Error in server communication: {e}")
            return EventNames.ERROR.name, f"Server communication error: {str(e)}"

    async def _handle_server_event(self, event):
        """Handle incoming events from clients"""
        if isinstance(event, HeadersReceived):
            # Log received headers
            logger.info(f"Server received headers: {event.headers}")
            
            # Send a response if this is a request
            response_headers = [
                (b':status', b'200'),
                (b'server', b'nopasaran-http3-server'),
                (b'content-type', b'text/plain')
            ]
            
            self.connection.send_headers(
                event.stream_id, 
                response_headers, 
                end_stream=False
            )
            
            # Send some response data
            response_data = b"Hello from HTTP/3 server"
            self.connection.send_data(
                event.stream_id, 
                response_data, 
                end_stream=True
            )
            
            self.protocol.transmit()
            
        elif isinstance(event, DataReceived):
            # Log received data
            logger.info(f"Server received data: {event.data}")

    async def stop(self):
        """Stop the HTTP/3 server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        await self.close()
        return EventNames.CONNECTION_CLOSED.name

