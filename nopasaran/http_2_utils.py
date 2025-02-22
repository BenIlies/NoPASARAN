import overload
import ssl
import logging
import socket
from typing import Dict, Any, Optional, Tuple, List
import h2
import json
import h2.events
import os
from datetime import datetime, timedelta
import argparse
import h2.connection
from hyperframe.frame import (
    HeadersFrame, DataFrame, GoAwayFrame, WindowUpdateFrame, 
    PingFrame, SettingsFrame, RstStreamFrame, PriorityFrame,
    ContinuationFrame
)
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import tempfile

class SSL_CONFIG:
    """SSL configuration constants"""
    CERT_PATH = "server.crt"
    KEY_PATH = "server.key"
    MAX_BUFFER_SIZE = 65535

def create_ssl_context(protocol='h2', is_client=True, cert_file=None, key_file=None):
    """Create SSL context with the specified protocol"""
    if is_client:
        ssl_context = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH
        )
        # For testing, disable certificate verification
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
    else:
        ssl_context = ssl.create_default_context(
            purpose=ssl.Purpose.CLIENT_AUTH
        )
        ssl_context.verify_mode = ssl.CERT_NONE  # Don't require client cert
    
    # Configure for HTTP/2
    ssl_context.set_alpn_protocols([protocol])
    
    if not is_client:
        # Server needs certificate and private key
        if cert_file and key_file:
            ssl_context.load_cert_chain(cert_file, key_file)
        else:
            # Generate temporary certificates if none provided
            temp_cert, temp_key = generate_temp_certificates()
            ssl_context.load_cert_chain(temp_cert, temp_key)
            # Clean up temporary files
            os.unlink(temp_cert)
            os.unlink(temp_key)
    
    # Additional security settings
    ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Only TLS 1.2+
    
    return ssl_context

def create_socket(host: str, port: int, is_server: bool = False):
    """Create and configure a socket"""
    sock = socket.socket()
    if is_server:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
    return sock

def handle_socket_error(logger: logging.Logger, error: Exception, context: str):
    """Handle socket-related errors"""
    logger.error(f"Socket error in {context}: {error}", exc_info=True)
    raise

def log_h2_frame(logger: logging.Logger, direction: str, event: Any):
    """Log HTTP/2 frame details"""
    event_type = event.__class__.__name__
    
    separator = "=" * 50
    logger.info(f"\n{separator}")
    logger.info(f"{direction} {event_type} FRAME")
    
    # Log basic frame info
    logger.info(f"Stream ID: {getattr(event, 'stream_id', 'N/A')}")
    
    # Add specific details based on frame type
    if isinstance(event, h2.events.RequestReceived):
        headers = dict(event.headers)
        logger.info("Headers:")
        for k, v in headers.items():
            logger.info(f"  {k}: {v}")
            
    elif isinstance(event, h2.events.ResponseReceived):
        headers = dict(event.headers)
        logger.info("Headers:")
        for k, v in headers.items():
            logger.info(f"  {k}: {v}")
            
    elif isinstance(event, h2.events.TrailersReceived):
        headers = dict(event.headers)
        logger.info("Trailers:")
        for k, v in headers.items():
            logger.info(f"  {k}: {v}")
            
    elif isinstance(event, h2.events.PushedStreamReceived):
        # Add PUSH_PROMISE specific logging
        logger.info(f"Parent Stream ID: {event.parent_stream_id}")
        logger.info(f"Pushed Stream ID: {event.pushed_stream_id}")
        headers = dict(event.headers)
        logger.info("Push Promise Headers:")
        for k, v in headers.items():
            logger.info(f"  {k}: {v}")
            
    elif isinstance(event, h2.events.SettingsAcknowledged):
        logger.info("Settings: ACK received")
        
    elif isinstance(event, h2.events.RemoteSettingsChanged):
        logger.info("Changed Settings:")
        for setting, value in event.changed_settings.items():
            if isinstance(setting, int):
                setting_name = setting
            else:
                setting_name = setting.name
            logger.info(f"  {setting_name}: {value}")
            
    elif isinstance(event, h2.events.WindowUpdated):
        logger.info(f"Window Update Delta: {event.delta}")
        
    elif isinstance(event, h2.events.DataReceived):
        logger.info(f"Data Length: {len(event.data)}")
        logger.info(f"Flow Controlled Length: {event.flow_controlled_length}")
        
    elif isinstance(event, h2.events.PriorityUpdated):
        logger.info(f"Depends On: {event.depends_on}")
        logger.info(f"Weight: {event.weight}")
        logger.info(f"Exclusive: {event.exclusive}")
        
    elif isinstance(event, h2.events.StreamReset):
        logger.info(f"Error Code: {event.error_code}")
        logger.info(f"Remote Reset: {event.remote_reset}")
        
    elif isinstance(event, h2.events.StreamEnded):
        logger.info("Stream Ended")
        
    logger.info(separator)

def load_test_case(logger: logging.Logger, test_id: int):
    """Load a specific test case by ID from the test cases file"""
    try:
        with open('tests/test_cases.json', 'r') as f:
            test_data = json.load(f)
            
        # Search through all test suites for the specified test ID
        for test_case in test_data:
            if test_case['id'] == test_id:
                logger.info(f"\nLoaded test case {test_id}:")
                logger.info(f"Description: {test_case['description']}\n")
                return test_case
                    
        logger.error(f"Test case with ID {test_id} not found")
        return None
        
    except FileNotFoundError:
        logger.error("test_cases.json file not found")
        return None
    except json.JSONDecodeError:
        logger.error("Error parsing test_cases.json")
        return None
    
# Default H2Configuration settings
H2_CONFIG_SETTINGS = {
    'header_encoding': 'utf-8',
    'validate_inbound_headers': False,
    'validate_outbound_headers': False,
    'normalize_inbound_headers': False,
    'normalize_outbound_headers': False,
}

def format_headers(headers_dict: Dict):
    """Convert headers dictionary to h2 compatible format
    Args:
        headers_dict: Dictionary containing pseudo_headers and regular_headers
    Returns:
        List of (name, value) tuples in correct order
    """
    headers = []
    
    for name, value in headers_dict.items():
        headers.append((name, str(value)))
        
    return headers

def send_frame(conn: h2.connection.H2Connection, sock: socket.socket, 
               frame_data: Dict):
    """Send a single H2 frame
    Args:
        conn: H2Connection instance
        sock: Socket to send data on
        frame_data: Frame configuration from test case
        logger: Logger instance
    """
    frame_type = frame_data.get('type')
    
    if frame_type == 'HEADERS':
        send_headers_frame(conn, sock, frame_data)
    elif frame_type == 'DATA':
        send_data_frame(conn, frame_data)
    elif frame_type == 'UNKNOWN':
        send_unknown_frame(sock, frame_data)
    elif frame_type == 'RST_STREAM':
        send_rst_stream_frame(conn, sock, frame_data)
    elif frame_type == 'PRIORITY':
        send_priority_frame(conn, sock, frame_data)
    elif frame_type == 'SETTINGS':
        send_settings_frame(conn, sock, frame_data)
    elif frame_type == 'PUSH_PROMISE':
        send_push_promise_frame(conn, sock, frame_data)
    elif frame_type == 'PING':
        send_ping_frame(conn, sock, frame_data)
    elif frame_type == 'GOAWAY':
        send_goaway_frame(conn, sock, frame_data)
    elif frame_type == 'WINDOW_UPDATE':
        send_window_update_frame(conn, sock, frame_data)
    elif frame_type == 'CONTINUATION':
        send_continuation_frame(conn, sock, frame_data)
    elif frame_type == 'TRAILERS':
        send_trailers_frame(conn, sock, frame_data)
    
    # Send any pending data
    outbound_data = conn.data_to_send()
    if outbound_data:
        sock.sendall(outbound_data)

def send_headers_frame(conn: h2.connection.H2Connection, sock, frame_data: Dict) -> None:
    """Send a HEADERS frame
    
    Args:
        conn: H2Connection instance
        sock: Socket to send data on
        frame_data: Frame configuration dictionary containing:
            - stream_id (optional): Stream ID
            - headers (optional): Headers to send
            - flags (optional): Dictionary containing:
                - END_STREAM (optional): Whether to end the stream
                - END_HEADERS (optional): Whether to end the headers
        - id: Test case ID
    """
    stream_id = frame_data.get('stream_id', 1)
    headers = frame_data.get('headers')
    duplicate_headers = frame_data.get('duplicate_headers')

    if headers:
        headers = format_headers(headers)
    else:
        headers = [(':method', 'GET'), (':path', '/'), (':authority', 'localhost'), (':scheme', 'http')]
    
    if duplicate_headers:
        duplicate_headers = format_headers(duplicate_headers)
        headers.extend(duplicate_headers)
        
    flags = frame_data.get('flags', {})
    end_stream = flags.get('END_STREAM', True)
    end_headers = flags.get('END_HEADERS', True)
    
    if frame_data.get('reserved_bit') or frame_data.get('raw_frame'):
        # Get encoded headers data
        encoded_headers = conn.encoder.encode(headers)
        
        # Construct frame header bytes
        length = len(encoded_headers)
        type_byte = 0x1  # HEADERS frame type
        frame_flags = 0x4  # END_HEADERS
        if end_stream:
            frame_flags |= 0x1  # END_STREAM
        if end_headers:
            frame_flags |= 0x4  # END_HEADERS
            
        # Create the length field (24 bits)
        length_bytes = length.to_bytes(3, byteorder='big')
        
        # Create type and flags bytes
        type_byte = type_byte.to_bytes(1, byteorder='big')
        flags_byte = frame_flags.to_bytes(1, byteorder='big')
        
        # Create stream ID with reserved bit
        # If reserved_bit is True, set highest bit to 1
        if frame_data.get('reserved_bit'):
            stream_id |= (1 << 31)  # Set the highest bit
        stream_id_bytes = stream_id.to_bytes(4, byteorder='big')
        
        # Combine all parts
        frame_header = length_bytes + type_byte + flags_byte + stream_id_bytes
        frame = frame_header + encoded_headers
        
        sock.sendall(frame)
        
        conn.state_machine.process_input(h2.connection.ConnectionInputs.SEND_HEADERS)
    else:
        if end_headers == False:
            frame = HeadersFrame(stream_id)
            frame.data = conn.encoder.encode(headers)
            
            if end_stream:
                frame.flags.add('END_STREAM')
            if end_headers:
                frame.flags.add('END_HEADERS')
            
            # Serialize and send
            serialized = frame.serialize()
            sock.sendall(serialized)
        else:
            conn.send_headers(
                stream_id=stream_id,
                headers=headers,
                end_stream=end_stream
            )

def send_trailers_frame(conn: h2.connection.H2Connection, sock: socket.socket, frame_data: Dict):
    """Send a TRAILERS frame"""
    stream_id = frame_data.get('stream_id', 1)
    headers = frame_data.get('headers')
    end_stream = frame_data.get('flags', {}).get('END_STREAM', True)
    if headers:
        headers = format_headers(headers)
    else:
        headers = [('content-type', 'text/plain')]
    
    # trailer_frame = HeadersFrame(stream_id)
    # trailer_frame.data = conn.encoder.encode(headers)
    # trailer_frame.flags.add('END_HEADERS')
    # trailer_frame.flags.add('END_STREAM')

    conn.send_headers(
        stream_id=stream_id,
        headers=headers,
        end_stream=end_stream
    )
    
    # serialized = trailer_frame.serialize()
    # sock.sendall(serialized)

def send_data_frame(conn: h2.connection.H2Connection, frame_data: Dict) -> None:
    """Send a DATA frame"""
    stream_id = frame_data.get('stream_id', 1)
    flags = frame_data.get('flags', {})
    payload = frame_data.get('payload', 'test')
    payload_size = frame_data.get('payload_size', None)
    
    if payload_size:
        payload = b'x' * payload_size
    elif isinstance(payload, str):
        payload = payload.encode('utf-8')
    
    conn.send_data(
        stream_id=stream_id,
        data=payload,
        end_stream=flags.get('END_STREAM', True)
    )

def send_unknown_frame(sock: socket.socket, frame_data: Dict):
    """Send an UNKNOWN frame"""
    payload = frame_data.get('payload', '').encode('utf-8')
    frame_type_id = frame_data.get('frame_type_id')
    flags = frame_data.get('flags', [])
    flags_byte = sum(1 << i for i, flag in enumerate(flags))
    stream_id = frame_data.get('stream_id')
    
    # Frame header format:
    # Length (24 bits) | Type (8 bits) | Flags (8 bits) | R (1 bit) | Stream ID (31 bits)
    length = len(payload)
    header = (
        length.to_bytes(3, byteorder='big') +  # Length
        frame_type_id.to_bytes(1, byteorder='big') +  # Type
        flags_byte.to_bytes(1, byteorder='big') +  # Flags
        stream_id.to_bytes(4, byteorder='big')  # R bit is 0 + Stream ID
    )
            
    # Send raw frame
    sock.sendall(header + payload)

def send_rst_stream_frame(conn: h2.connection.H2Connection, sock: socket.socket, frame_data: Dict):
    """Send a RST_STREAM frame"""
    stream_id = frame_data.get('stream_id', 1)
    if frame_data.get('payload_length'):
        payload_length = frame_data.get('payload_length', 4)  # Default to valid length of 4
        payload = b'\x00' * payload_length
        header = (
            payload_length.to_bytes(3, byteorder='big') +  # Length
            b'\x03' +  # Type (0x3 for RST_STREAM)
            b'\x00' +  # Flags (none for RST_STREAM)
            stream_id.to_bytes(4, byteorder='big')  # Stream ID
        )
        frame = header + payload
    else:
        rsf = RstStreamFrame(stream_id)
        rsf.error_code = 0
        frame = rsf.serialize()
        
    sock.sendall(frame)

def send_priority_frame(conn, sock, frame_data):
    stream_id = frame_data.get('stream_id', 1)
    frame = PriorityFrame(stream_id)

    frame.stream_weight = frame_data.get('weight', 15)
    frame.depends_on = frame_data.get('depends_on', 0)
    frame.exclusive = frame_data.get('exclusive', False)

    frame = frame.serialize()
    sock.sendall(frame)

def send_settings_frame(conn: h2.connection.H2Connection, sock: socket.socket, frame_data: Dict):
    """Send a SETTINGS frame with optional stream ID"""
    settings = frame_data.get('settings', {})
    flags = frame_data.get('flags', {})
    stream_id = frame_data.get('stream_id', 0)  # Default to 0 as per spec
    
    # Convert settings keys to appropriate type (int or SettingCodes)
    processed_settings = {}
    for name, value in settings.items():
        # If it's already a number, use it directly
        if isinstance(name, int):
            processed_settings[name] = value
            continue
            
        # Try to convert string to int for numeric settings
        try:
            setting_id = int(name)
            processed_settings[setting_id] = value
        except ValueError:
            # If not numeric, treat as a valid setting name
            try:
                setting_id = getattr(h2.settings.SettingCodes, name)
                processed_settings[setting_id] = value
            except AttributeError:
                # If setting name doesn't exist, skip it
                continue
    
    # Always use raw frame sending if we have unknown settings or non-zero stream ID
    if (stream_id != 0 or 
        'extra_bytes' in frame_data or 
        'raw_payload' in frame_data):
        
        settings_payload = b''
        for setting_id, value in processed_settings.items():
            # Each setting is a 16-bit ID and 32-bit value
            settings_payload += setting_id.to_bytes(2, byteorder='big')
            settings_payload += value.to_bytes(4, byteorder='big')
        
        extra_payload = b'\x00' * frame_data.get('extra_bytes', 0)
        settings_payload += extra_payload
        length = len(settings_payload)
        
        # Frame header format:
        # Length (24 bits) | Type (8 bits) | Flags (8 bits) | R (1 bit) | Stream ID (31 bits)
        flags_byte = 0x1 if 'ACK' in flags else 0x0
        header = (
            length.to_bytes(3, byteorder='big') +  # Length
            b'\x04' +  # Type (0x4 for SETTINGS)
            flags_byte.to_bytes(1, byteorder='big') +  # Flags
            stream_id.to_bytes(4, byteorder='big')  # Stream ID
        )
        
        # Send raw frame
        sock.sendall(header + settings_payload)
    else:
        # Use h2's normal method for valid frames
        frame = SettingsFrame(stream_id=stream_id)
        
        # Add settings
        frame.settings.update(processed_settings)
        
        # Add flags if specified
        if 'ACK' in flags:
            frame.flags.add('ACK')
        
        # Serialize and send
        serialized = frame.serialize()
        sock.sendall(serialized)

def send_push_promise_frame(conn: h2.connection.H2Connection, sock: socket.socket, frame_data: Dict):
    """Send a PUSH_PROMISE frame"""
    stream_id = frame_data.get('stream_id', 1)
    promised_stream_id = frame_data.get('promised_stream_id', 2)
    headers = frame_data.get('headers')
    flags = frame_data.get('flags', {})
    end_headers = flags.get('END_HEADERS', True)
    end_stream = flags.get('END_STREAM', True)
    
    if headers:
        headers = format_headers(headers)
    else:
        headers = [(':method', 'GET'), (':path', '/'), (':authority', 'localhost'), (':scheme', 'http')]
    
    # Get encoded headers from the connection's encoder
    encoded_headers = conn.encoder.encode(headers)
    
    # Frame header format:
    # Length (24 bits) | Type (8 bits) | Flags (8 bits) | R (1 bit) | Stream ID (31 bits)
    # Followed by:
    # R (1 bit) | Promised Stream ID (31 bits) | Header Block Fragment
    
    # Calculate total length (4 bytes for promised stream ID + encoded headers)
    length = 4 + len(encoded_headers)
    
    # Create flags byte
    flags_byte = 0
    # END_HEADERS flag
    if end_headers:
        flags_byte |= 0x4
    # END_STREAM flag
    if end_stream:
        flags_byte |= 0x1
    
    # Create frame header
    header = (
        length.to_bytes(3, byteorder='big') +  # Length
        b'\x05' +  # Type (0x5 for PUSH_PROMISE)
        flags_byte.to_bytes(1, byteorder='big') +  # Flags
        stream_id.to_bytes(4, byteorder='big')  # Stream ID
    )
    
    # Create promised stream ID field (31 bits, with reserved bit)
    promised_stream_bytes = promised_stream_id.to_bytes(4, byteorder='big')
    
    # Combine all parts
    frame = header + promised_stream_bytes + encoded_headers
    
    # Send the frame
    sock.sendall(frame)

def send_ping_frame(conn: h2.connection.H2Connection, sock: socket.socket, frame_data: Dict):
    """Send a PING frame
    
    Args:
        conn: H2Connection instance
        sock: Socket to send data on
        frame_data: Frame configuration dictionary containing:
            - data (optional): 8 bytes of data to include in the PING
            - flags (optional): Dictionary of flags to set
    """
    flags = frame_data.get('flags', {})
    data = frame_data.get('data', b'\x00' * 8)  # Default to 8 zero bytes
    stream_id = frame_data.get('stream_id', 0)
    
    # Convert string data to bytes if necessary
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    frame = PingFrame(stream_id)
    frame.data = data
    
    # Add ACK flag if specified
    if 'ACK' in flags:
        frame.flags.add('ACK')
    
    # Serialize and send
    serialized = frame.serialize()
    sock.sendall(serialized)

def send_goaway_frame(conn: h2.connection.H2Connection, sock: socket.socket, frame_data: Dict):
    """Send a GOAWAY frame
    
    Args:
        conn: H2Connection instance
        sock: Socket to send data on
        frame_data: Frame configuration dictionary containing:
            - last_stream_id (optional): Last stream ID processed
            - error_code (optional): Error code to send (default: 0 - NO_ERROR)
            - additional_data (optional): Debug data to include
    """
    last_stream_id = frame_data.get('last_stream_id', 0)
    error_code = frame_data.get('error_code', 0)
    stream_id = frame_data.get('stream_id', 0)
    
    frame = GoAwayFrame(stream_id)
    frame.last_stream_id = last_stream_id
    frame.error_code = error_code
    
    # Serialize and send
    serialized = frame.serialize()
    sock.sendall(serialized)

def send_window_update_frame(conn: h2.connection.H2Connection, sock: socket.socket, frame_data: Dict):
    """Send a WINDOW_UPDATE frame
    
    Args:
        conn: H2Connection instance
        sock: Socket to send data on
        frame_data: Frame configuration dictionary containing:
            - stream_id (optional): Stream ID (0 for connection-level updates)
            - increment (optional): Window size increment (default: 1024)
    """
    stream_id = frame_data.get('stream_id', 0)
    increment = frame_data.get('increment', 1024)
    
    frame = WindowUpdateFrame(stream_id)
    frame.window_increment = increment
    
    # Serialize and send
    serialized = frame.serialize()
    sock.sendall(serialized)

def send_continuation_frame(conn: h2.connection.H2Connection, sock: socket.socket, frame_data: Dict):
    """Send a CONTINUATION frame
    
    Args:
        conn: H2Connection instance
        sock: Socket to send data on
        frame_data: Frame configuration dictionary containing:
            - stream_id (required): Stream ID (must match the stream of preceding HEADERS/PUSH_PROMISE)
            - headers (optional): Additional headers to send
            - flags (optional): Dictionary of flags to set
            - end_headers (optional): Whether this is the last CONTINUATION frame (default: True)
    """
    stream_id = frame_data.get('stream_id')
    headers = frame_data.get('headers')
    flags = frame_data.get('flags', {})
    end_headers = flags.get('END_HEADERS', True)
    
    # Format and encode headers
    if headers:
        headers = format_headers(headers)
    else:
        headers = [('accept-encoding', 'gzip, deflate, br')]

    encoded_headers = conn.encoder.encode(headers)
    
    frame = ContinuationFrame(stream_id)
    frame.data = encoded_headers
    
    # Set END_HEADERS flag if this is the last CONTINUATION frame
    if end_headers:
        frame.flags.add('END_HEADERS')
    
    # Serialize and send
    serialized = frame.serialize()
    sock.sendall(serialized)

def generate_temp_certificates():
    """Generate temporary self-signed certificates for TLS testing"""
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Generate certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u"test.nopasaran.com"),  # Simple test domain
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Test Certificate"),
    ])

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=1)
    ).sign(private_key, hashes.SHA256())

    # Create temporary files
    cert_file = tempfile.NamedTemporaryFile(delete=False)
    key_file = tempfile.NamedTemporaryFile(delete=False)

    # Write certificate and private key to temporary files
    cert_file.write(cert.public_bytes(serialization.Encoding.PEM))
    key_file.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

    cert_file.close()
    key_file.close()

    return cert_file.name, key_file.name