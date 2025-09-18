import overload
import ssl
import socket
from typing import Dict, Any, Optional, Tuple, List
import h2
import json
import h2.events
import os
from datetime import datetime, timedelta, timezone
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
import io

class SSL_CONFIG:
    """SSL configuration constants"""
    MAX_BUFFER_SIZE = 65535

# Define your certificates as string constants
EMBEDDED_CERT = """-----BEGIN CERTIFICATE-----
MIIEpDCCA4ygAwIBAgIUCAI1jMFNjYW42UodjkGwsETOOUYwDQYJKoZIhvcNAQEL
BQAwgYsxCzAJBgNVBAYTAlVTMRkwFwYDVQQKExBDbG91ZEZsYXJlLCBJbmMuMTQw
MgYDVQQLEytDbG91ZEZsYXJlIE9yaWdpbiBTU0wgQ2VydGlmaWNhdGUgQXV0aG9y
aXR5MRYwFAYDVQQHEw1TYW4gRnJhbmNpc2NvMRMwEQYDVQQIEwpDYWxpZm9ybmlh
MB4XDTI1MDIyNTEwMjYwMFoXDTQwMDIyMjEwMjYwMFowYjEZMBcGA1UEChMQQ2xv
dWRGbGFyZSwgSW5jLjEdMBsGA1UECxMUQ2xvdWRGbGFyZSBPcmlnaW4gQ0ExJjAk
BgNVBAMTHUNsb3VkRmxhcmUgT3JpZ2luIENlcnRpZmljYXRlMIIBIjANBgkqhkiG
9w0BAQEFAAOCAQ8AMIIBCgKCAQEArXyMWbyWYTiAFNmEIf5cE/3PAxSjGGonKEs3
Ppn6effRgxwYTQLsdiVzXxgaKDEklUWwn0diWVX3eOym27O1EDwsJJHAsz+ph7pz
c3b0FIMW2XoRFBczmsj3Jh3JBE61GlHfPIFPB3adO+e8kgoRg9Ac7vWGYkz9TY3n
QH0locAHbziITua4FrPvrJEUot3bTdF6KmX20hDccSThKNi1xKbgfkFYsv/k9/jS
aV/mbQVuxIIcKavAc/E2jD7M671m7TZkzcp0fVLxdQgO6YO4PoQS7prZTn+ORJZT
UzlMypwf4bwAQsY0lZRdWKaSsngmXXRVoJI/C1cbXZHy35EmhQIDAQABo4IBJjCC
ASIwDgYDVR0PAQH/BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMCBggrBgEFBQcD
ATAMBgNVHRMBAf8EAjAAMB0GA1UdDgQWBBQGdwBYQgTA3nHOX0nL+H/XUGgd8jAf
BgNVHSMEGDAWgBQk6FNXXXw0QIep65TbuuEWePwppDBABggrBgEFBQcBAQQ0MDIw
MAYIKwYBBQUHMAGGJGh0dHA6Ly9vY3NwLmNsb3VkZmxhcmUuY29tL29yaWdpbl9j
YTAnBgNVHREEIDAegg4qLm5vcGFzYXJhbi5jb4IMbm9wYXNhcmFuLmNvMDgGA1Ud
HwQxMC8wLaAroCmGJ2h0dHA6Ly9jcmwuY2xvdWRmbGFyZS5jb20vb3JpZ2luX2Nh
LmNybDANBgkqhkiG9w0BAQsFAAOCAQEASOEB3ZP9LSXkhhdLD0bVACC3EAdefJmm
v510EvT4lBKGYSOn7aiTAzjihlOhBWXR9TkZov+JtJXD8Dsq1pAy4bB7kDn+fhAE
j6NtM0dKW8yfz6wYB567Cmi0TNoeS0hzCEarTjQEYEwbZN/KZ2KX28nwEtywC5W7
5SaFHsjcpotV53erxxZmUGG9ZGeQhKXtlQHcISqF7JBYNSO0cViR25eS38l7q5Tk
J6Xw/ti3A85jfeUp0vRlBb4EKAWP2FG9UPvzBVFolCJ4Rt4s44H8LCWuvBeC9Dkj
XqFXTLBnd0nQn407YrW+1EoLSch/bxkE5f6RBOnZ2fgTVvFdawj7oQ==
-----END CERTIFICATE-----"""

EMBEDDED_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCtfIxZvJZhOIAU
2YQh/lwT/c8DFKMYaicoSzc+mfp599GDHBhNAux2JXNfGBooMSSVRbCfR2JZVfd4
7Kbbs7UQPCwkkcCzP6mHunNzdvQUgxbZehEUFzOayPcmHckETrUaUd88gU8Hdp07
57ySChGD0Bzu9YZiTP1NjedAfSWhwAdvOIhO5rgWs++skRSi3dtN0XoqZfbSENxx
JOEo2LXEpuB+QViy/+T3+NJpX+ZtBW7Eghwpq8Bz8TaMPszrvWbtNmTNynR9UvF1
CA7pg7g+hBLumtlOf45EllNTOUzKnB/hvABCxjSVlF1YppKyeCZddFWgkj8LVxtd
kfLfkSaFAgMBAAECggEAKriZbT2qAG3j6H558c8LyKZ/NECAOzJkyyDejU1op2FV
2AXynABEz4FAbGHoiw4y9olPSaHP/7TSOJZ6Lm8N/t36dtTnkZxzOGe7J2tbBrQT
S+Gp0/s0q4Cij+HUzvk80qrnoKQtHGbiqE5UGthc4Ms+XL/cZFeWJuNzV2eZ/T79
/q8WgQQ/eFkbg+raYXtSV3ntPka6qmMzpzP3WbmcHfVlZWIRHyS54yE0QgdQl6uF
ZN+d6DbLEj2NFEWVNJWxv3Sq3gMOfbooLjsbwO8U7XetVuFfMpfRUiN7k/ADb0kK
mbulpLcJtthpNio/rY6e69wFaBapoRbgD/c7bMpw7wKBgQD04wRVGSnQIsZBqhIz
tmwV+Lr8ZetxsJ0GscDAEIDYKwha3UO6L/ODqQG0kTyU3HsmQUISNBrv7hcy5Fos
JOfkeYLrFnoMobdM+lGeBRZXvjpBcSjTBJl5I+ddMvD/8OESf9IOeMAvtjw0yoCH
4UvwVWWkkyKRb/pxgpeK1XCjRwKBgQC1XAkZHz+hdSD5UUWV9YvgLN0e0XJgHwUI
jqzHkCONkFTXlDrRPtFCZvzmetUdF1DR1GlTNTgvZ63ItoAC6Jdm4VZfSTZd9oRF
MacH10mh8R40+NJx1pe22z1dgy9RiH+LkuDHHubhtvKzI3DggaX3KPcntCLaCMZY
pBSlIFxV0wKBgEXyHcess0u20wfoauCIZ2DzNX1oIxLLDl7eIJ77V8HmsLE7Z9/j
WFuvx0PrA/HE9AveMd//L/598/ReUv8u32lb56/8MIoxGqkLCornCxWuyPbuOmnj
c26teaUeKsX/6FmfVsE5bjNyisnNWV72U/lmeuzB9eqyoEcRtPU7t7t7AoGAUJxq
BtqW4+M2FtuC/Ja555jJaEtcdVEUYatZLRLqWqAOtgvS4PL0/HjebGuoklesureZ
YTzEjn2dBxvnZmOP+FCsnYnjOny6ai8ZuSh+OBb+gDkhASyLHuHwMsJ+o9TyLE3K
z3by1N0Gn41fPMsjw+pXgTRWUWeZEglMi+EIabUCgYBEf2hU27W6jiYOUf081oFK
uVBdI0M1WSIMIaHkTWAbIBpvbYs6HPg3ahNL328fOgw2REwNqbdWhrkaXSDFuEOa
lLYvHR05hvsABWzD7a4+VBt1wALrLvckl8zZIFYrY8B3KIjpcJI+SYmuZKEDNFFz
Y/ryzgff8qQY7HLuCVsj5g==
-----END PRIVATE KEY-----"""

def create_ssl_context(is_client=False, use_embedded_certs=False):
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
    
    ssl_context.set_alpn_protocols(['h2'])

    keylog_path = os.path.join(os.getcwd(), 'nopasaran_sslkeys.log')
    try:
        if hasattr(ssl_context, 'keylog_filename'):
            ssl_context.keylog_filename = keylog_path
    except Exception:
        pass
    
    if not is_client:
        if use_embedded_certs:
            # Use the embedded certificates
            ssl_context = load_embedded_certificates(ssl_context)
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
               frame_data: Dict, is_server: bool = False, cloudflare_origin: bool = False):
    """Send a single H2 frame
    Args:
        conn: H2Connection instance
        sock: Socket to send data on
        frame_data: Frame configuration from test case
        is_server: Whether the frame is being sent from the server
        cloudflare_origin: Whether the frame is being sent from the cloudflare origin
    """
    frame_type = frame_data.get('type')
    
    if frame_type == 'HEADERS':
        send_headers_frame(conn, sock, frame_data, is_server, cloudflare_origin)
    elif frame_type == 'DATA':
        send_data_frame(conn, frame_data, is_server, cloudflare_origin)
    elif frame_type == 'UNKNOWN':
        send_unknown_frame(sock, frame_data, cloudflare_origin)
    elif frame_type == 'RST_STREAM':
        send_rst_stream_frame(conn, sock, frame_data, cloudflare_origin)
    elif frame_type == 'PRIORITY':
        send_priority_frame(conn, sock, frame_data, cloudflare_origin)
    elif frame_type == 'SETTINGS':
        send_settings_frame(conn, sock, frame_data)
    elif frame_type == 'PUSH_PROMISE':
        send_push_promise_frame(conn, sock, frame_data, cloudflare_origin)
    elif frame_type == 'PING':
        send_ping_frame(conn, sock, frame_data)
    elif frame_type == 'GOAWAY':
        send_goaway_frame(conn, sock, frame_data)
    elif frame_type == 'WINDOW_UPDATE':
        send_window_update_frame(conn, sock, frame_data)
    elif frame_type == 'CONTINUATION':
        send_continuation_frame(conn, sock, frame_data, cloudflare_origin)
    elif frame_type == 'TRAILERS':
        send_trailers_frame(conn, sock, frame_data, cloudflare_origin)
    
    # Send any pending data
    outbound_data = conn.data_to_send()
    if outbound_data:
        sock.sendall(outbound_data)

def send_headers_frame(conn: h2.connection.H2Connection, sock, frame_data: Dict, is_server: bool = False, cloudflare_origin: bool = False) -> None:
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
    # next_legal_id = conn.get_next_available_stream_id()
    stream_id = frame_data.get('stream_id', 3 if cloudflare_origin else 1)
    headers = frame_data.get('headers')
    duplicate_headers = frame_data.get('duplicate_headers')

    if headers:
        headers = format_headers(headers)
    else:
        if is_server:
            headers = [(':status', '200'), ('content-type', 'text/plain'), ('server', 'nopasaran-http2-server'), ('date', datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT'))]
        else:
            headers = [(':method', 'GET'), (':path', '/test-frame'), (':authority', conn.host), (':scheme', conn.scheme), ('user-agent', 'nopasaran-http2-client'), ('accept', '*/*')]
    
    if duplicate_headers:
        duplicate_headers = format_headers(duplicate_headers)
        headers.extend(duplicate_headers)
        
    flags = frame_data.get('flags', {})
    end_stream = flags.get('END_STREAM', False)
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

def send_trailers_frame(conn: h2.connection.H2Connection, sock: socket.socket, frame_data: Dict, cloudflare_origin: bool = False):
    """Send a TRAILERS frame"""
    stream_id = frame_data.get('stream_id', 3 if cloudflare_origin else 1)
    headers = frame_data.get('headers', [])
    end_stream = frame_data.get('flags', {}).get('END_STREAM', True)
    if headers != []:
        headers = format_headers(headers)
    else:
        headers = [('x-extra-info', 'some trailer info')]
    
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

def send_data_frame(conn: h2.connection.H2Connection, frame_data: Dict, is_server: bool = False, cloudflare_origin: bool = False) -> None:
    """Send a DATA frame"""
    stream_id = frame_data.get('stream_id', 3 if cloudflare_origin else 1)
    flags = frame_data.get('flags', {})
    payload = frame_data.get('payload', 'Hello from server!' if is_server else 'Hello from client!')
    payload_size = frame_data.get('payload_size', None)
    
    if payload_size:
        payload = b'x' * payload_size
    elif isinstance(payload, str):
        payload = payload.encode('utf-8')
    
    conn.send_data(
        stream_id=stream_id,
        data=payload,
        end_stream=flags.get('END_STREAM', False)
    )

def send_unknown_frame(sock: socket.socket, frame_data: Dict, cloudflare_origin: bool = False):
    """Send an UNKNOWN frame"""
    payload = frame_data.get('payload', 'test payload').encode('utf-8')
    frame_type_id = frame_data.get('frame_type_id', '99')
    flags = frame_data.get('flags', [])
    flags_byte = sum(1 << i for i, flag in enumerate(flags))
    stream_id = frame_data.get('stream_id', 3 if cloudflare_origin else 1)
    
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

def send_rst_stream_frame(conn: h2.connection.H2Connection, sock: socket.socket, frame_data: Dict, cloudflare_origin: bool = False):
    """Send a RST_STREAM frame"""
    stream_id = frame_data.get('stream_id', 3 if cloudflare_origin else 1)
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

def send_priority_frame(conn, sock, frame_data, cloudflare_origin: bool = False):
    stream_id = frame_data.get('stream_id', 3 if cloudflare_origin else 1)
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

def send_push_promise_frame(conn: h2.connection.H2Connection, sock: socket.socket, frame_data: Dict, cloudflare_origin: bool = False):
    """Send a PUSH_PROMISE frame"""
    stream_id = frame_data.get('stream_id', 3 if cloudflare_origin else 1)
    promised_stream_id = frame_data.get('promised_stream_id', 4 if cloudflare_origin else 2)
    headers = frame_data.get('headers')
    flags = frame_data.get('flags', {})
    end_headers = flags.get('END_HEADERS', True)
    end_stream = flags.get('END_STREAM', False)
    
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

def send_continuation_frame(conn: h2.connection.H2Connection, sock: socket.socket, frame_data: Dict, cloudflare_origin: bool = False):
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
    stream_id = frame_data.get('stream_id', 3 if cloudflare_origin else 1)
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

def load_embedded_certificates(ssl_context):
    """Load embedded certificates by writing to temporary files"""
    # Create temporary files for the certificates
    with tempfile.NamedTemporaryFile(delete=False, suffix='.crt') as cert_temp:
        cert_temp.write(EMBEDDED_CERT.encode('utf-8'))
        cert_temp_path = cert_temp.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.key') as key_temp:
        key_temp.write(EMBEDDED_KEY.encode('utf-8'))
        key_temp_path = key_temp.name
    
    # Load the certificate and key from the temporary files
    ssl_context.load_cert_chain(
        certfile=cert_temp_path,
        keyfile=key_temp_path
    )
    
    # Clean up the temporary files
    os.unlink(cert_temp_path)
    os.unlink(key_temp_path)
    
    return ssl_context