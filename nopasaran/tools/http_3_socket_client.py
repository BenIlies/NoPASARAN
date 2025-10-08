import asyncio
import logging
import time
from typing import Dict, List, Optional, Tuple, Any
from aioquic.asyncio import QuicConnectionProtocol, connect
from aioquic.h3.connection import H3Connection
from aioquic.h3.events import H3Event, HeadersReceived, DataReceived
from aioquic.quic.events import QuicEvent
from nopasaran.definitions.events import EventNames
from nopasaran.http_3_utils import create_quic_configuration
from nopasaran.tools.http_3_socket_base import HTTP3SocketBase, EventCapturingProtocol
import nopasaran.tools.http_3_overwrite

logger = logging.getLogger("http3_client")

class HTTP3SocketClient(HTTP3SocketBase):
    """HTTP/3 client implementation with deterministic frame injection support"""

    async def start(self):
        """Start the HTTP/3 client"""
        try:
            # Create QUIC configuration (TLS always enabled for HTTP/3, SSL key logging always enabled for client)
            import ssl
            configuration = create_quic_configuration(
                is_client=True,
                verify_mode=ssl.CERT_NONE  # Required for self-signed certificates (e.g., Caddy local_certs)
            )
            
            # Connect to server
            self._protocol_context = connect(
                self.host,
                self.port,
                configuration=configuration,
                create_protocol=EventCapturingProtocol,
            )
            
            self.protocol = await self._protocol_context.__aenter__()
            self.connection = H3Connection(self.protocol._quic)
            
            # Add connection attributes
            self.connection.host = self.host
            self.connection.scheme = 'https'  # HTTP/3 always uses HTTPS
            
            # Wait for connection to be established and verify it's ready
            await asyncio.sleep(0.5)
            
            # Verify connection is established
            if not self.protocol or not self.protocol._quic:
                return EventNames.ERROR.name, f"Failed to establish QUIC connection to {self.host}:{self.port}"
                
            # Wait for handshake completion with faster failure detection
            max_wait = 5.0
            wait_time = 0.0
            last_crypto_count = 0
            retransmit_cycles = 0
            
            while wait_time < max_wait and not self.protocol._quic._handshake_complete:
                await asyncio.sleep(0.1)
                wait_time += 0.1
                
                # Check if connection was closed by peer during handshake
                if hasattr(self.protocol._quic, '_close_event') and self.protocol._quic._close_event:
                    close_event = self.protocol._quic._close_event
                    error_code = getattr(close_event, 'error_code', None)
                    reason = getattr(close_event, 'reason_phrase', '')
                    
                    # Extract TLS alert if this is a CRYPTO_ERROR (0x100-0x1FF range)
                    if isinstance(error_code, int) and 0x100 <= error_code <= 0x1FF:
                        tls_alert = error_code & 0xFF
                        tls_alert_names = {
                            80: "internal_error",
                            40: "handshake_failure",
                            42: "bad_certificate",
                            43: "unsupported_certificate",
                            70: "protocol_version",
                            71: "insufficient_security",
                        }
                        alert_name = tls_alert_names.get(tls_alert, f"alert_{tls_alert}")
                        return EventNames.ERROR.name, f"Proxy rejected TLS handshake with {alert_name} (error {hex(error_code)}). Proxy may have incompatible TLS 1.3 configuration or doesn't support aioquic's cipher suites."
                    
                    if error_code is not None:
                        return EventNames.ERROR.name, f"Connection closed by proxy during handshake (error {hex(error_code) if isinstance(error_code, int) else error_code}, reason: '{reason}')"
                
                # Detect retransmission loop (proxy not responding)
                if hasattr(self.protocol._quic, '_crypto_retransmitted_data'):
                    current_crypto_count = len(self.protocol._quic._crypto_retransmitted_data)
                    if current_crypto_count > last_crypto_count:
                        retransmit_cycles += 1
                        last_crypto_count = current_crypto_count
                        
                        # If we've retransmitted 3+ times, proxy likely doesn't support HTTP/3
                        if retransmit_cycles >= 3:
                            return EventNames.ERROR.name, f"Proxy at {self.host}:{self.port} not responding to QUIC handshake (likely doesn't support HTTP/3 or UDP is blocked)"
                
            if not self.protocol._quic._handshake_complete:
                return EventNames.ERROR.name, f"QUIC handshake did not complete within {max_wait}s - proxy may not support HTTP/3"
            
            selected_protocol = 'h3'  # HTTP/3 always uses h3
            return EventNames.CLIENT_STARTED.name, f"Client successfully connected to {self.host}:{self.port} with TLS and ALPN protocol {selected_protocol}."
                
        except asyncio.TimeoutError:
            return EventNames.ERROR.name, f"Timeout occurred after {self.TIMEOUT}s while trying to connect to server at {self.host}:{self.port}"
        except ConnectionRefusedError as e:
            return EventNames.ERROR.name, f"Connection refused by server at {self.host}:{self.port}. Server may not be running or port may be blocked: {e}"
        except Exception as e:
            # Check if connection was closed with TLS error before generic fallback
            if self.protocol and hasattr(self.protocol, '_quic') and hasattr(self.protocol._quic, '_close_event'):
                close_event = self.protocol._quic._close_event
                if close_event:
                    error_code = getattr(close_event, 'error_code', None)
                    reason = getattr(close_event, 'reason_phrase', '')
                    
                    # Extract TLS alert if this is a CRYPTO_ERROR (0x100-0x1FF range)
                    if isinstance(error_code, int) and 0x100 <= error_code <= 0x1FF:
                        tls_alert = error_code & 0xFF
                        tls_alert_names = {
                            80: "internal_error",
                            40: "handshake_failure",
                            42: "bad_certificate",
                            43: "unsupported_certificate",
                            70: "protocol_version",
                            71: "insufficient_security",
                        }
                        alert_name = tls_alert_names.get(tls_alert, f"alert_{tls_alert}")
                        return EventNames.ERROR.name, f"Proxy rejected TLS handshake with {alert_name} (error {hex(error_code)}). Reason: {reason if reason else 'none'}. Proxy may have incompatible TLS 1.3 configuration."
                    
                    if error_code is not None:
                        return EventNames.ERROR.name, f"Connection closed by proxy (error {hex(error_code) if isinstance(error_code, int) else error_code}, reason: {reason if reason else 'none'})"
            
            # Generic error fallback
            return EventNames.ERROR.name, f"Error connecting to {self.host}:{self.port}: {str(e)}"

    async def run_communication(self, frame_spec: Dict[str, Any] = None):
        """
        Run client-side HTTP/3 communication with optional deterministic frame injection.
        
        Args:
            frame_spec: Dictionary containing client_frames and server_frames to inject
        """
        if frame_spec:
            self.set_deterministic_frames(frame_spec)
        
        try:
            # Send deterministic client frames if configured
            if hasattr(self, 'deterministic_frames') and self.deterministic_frames and "client_frames" in self.deterministic_frames:
                result = await self.send_deterministic_frames("client_frames")
                logger.info(f"Sent deterministic client frames: {result}")
            else:
                # Send a normal HTTP/3 request
                await self._send_normal_request()
            
            # Listen for server responses
            await self._listen_for_responses()
            
            return EventNames.FRAMES_SENT.name, "Client communication completed successfully"
            
        except Exception as e:
            logger.error(f"Error in client communication: {e}")
            return EventNames.ERROR.name, f"Client communication error: {str(e)}"

    async def _send_normal_request(self):
        """Send a normal HTTP/3 request"""
        try:
            # Verify connection is ready
            if not self.protocol or not self.connection:
                raise Exception("Connection not established")
                
            # Get next available stream
            stream_id = self.protocol._quic.get_next_available_stream_id()
            
            # Send headers for a normal GET request
            headers = [
                (b':method', b'GET'),
                (b':path', b'/'),
                (b':scheme', self.connection.scheme.encode()),
                (b':authority', self.host.encode()),
                (b'user-agent', b'nopasaran-http3-client'),
            ]
            
            self.connection.send_headers(stream_id, headers, end_stream=True)
            self.protocol.transmit()
            
            logger.info(f"Sent normal HTTP/3 request on stream {stream_id}")
        except Exception as e:
            logger.error(f"Failed to send normal request: {e}")
            raise

    async def _listen_for_responses(self):
        """Listen for responses from the server"""
        timeout_start = time.time()
        
        while time.time() - timeout_start < self.TIMEOUT:
            events = await self._receive_frame(timeout=1.0)
            
            if events:
                for event in events:
                    if isinstance(event, HeadersReceived):
                        logger.info(f"Client received headers: {event.headers}")
                    elif isinstance(event, DataReceived):
                        logger.info(f"Client received data: {event.data}")
            
            await asyncio.sleep(0.01)

    async def close(self):
        """Close the HTTP/3 client connection"""
        try:
            if hasattr(self, '_protocol_context'):
                await self._protocol_context.__aexit__(None, None, None)
            
            return await super().close()
        except Exception as e:
            return EventNames.ERROR.name
