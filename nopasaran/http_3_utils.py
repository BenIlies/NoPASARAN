import ssl
import socket
import os
from typing import Dict, Any
from aioquic.quic.configuration import QuicConfiguration
from nopasaran.http_2_utils import generate_temp_certificates

# HTTP/3 configuration settings
H3_CONFIG_SETTINGS = {
    'max_datagram_frame_size': 65536,
    'max_stream_data': 1048576,
    'max_data': 10485760,
}

# SSL configuration for HTTP/3
class SSL_CONFIG:
    MAX_BUFFER_SIZE = 65535
    CERT_FILE = None
    KEY_FILE = None

def create_ssl_context(is_client=True):
    """Create SSL context for HTTP/3 connections"""
    context = ssl.create_default_context()
    
    if is_client:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    else:
        # Server configuration
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    
    # Set ALPN protocols for HTTP/3
    context.set_alpn_protocols(['h3'])
    
    return context

def get_default_secrets_log_file():
    """Get the default path for SSL key logging file"""
    return os.path.join(os.getcwd(), 'nopasaran_http3_sslkeys.log')

def create_quic_configuration(is_client=True, verify_mode=None, secrets_log_file=None):
    """Create QUIC configuration for HTTP/3 with SSL key logging enabled by default for clients"""
    if verify_mode is None:
        verify_mode = ssl.CERT_NONE if is_client else ssl.CERT_REQUIRED
        
    config = QuicConfiguration(
        is_client=is_client,
        alpn_protocols=["h3"],
        verify_mode=verify_mode,
        idle_timeout=5.0,
        # Make QUIC parameters more permissive for proxy compatibility
        max_datagram_frame_size=65536
    )
    
    # Enable SSL key logging only for clients
    if is_client:
        if secrets_log_file is None:
            secrets_log_file = get_default_secrets_log_file()
            
        try:
            # Ensure the log file can be created/opened
            with open(secrets_log_file, 'a'):
                pass
            config.secrets_log_file = open(secrets_log_file, 'a')
        except Exception:
            # If we can't create/write to the log file, try a fallback location
            try:
                fallback_file = os.path.join(os.path.expanduser("~"), 'nopasaran_http3_sslkeys.log')
                with open(fallback_file, 'a'):
                    pass
                config.secrets_log_file = open(fallback_file, 'a')
            except Exception:
                # If all fails, proceed without logging but don't crash
                pass
    
    # Configure certificates for server
    if not is_client:
        # Generate temporary certificates for server
        temp_cert, temp_key = generate_temp_certificates()
        config.load_cert_chain(temp_cert, temp_key)
        
        # Clean up temporary files
        import os
        os.unlink(temp_cert)
        os.unlink(temp_key)
    
    return config


def create_socket(host: str, port: int, is_server=False):
    """Create socket for HTTP/3 connections"""
    if is_server:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        return sock
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return sock