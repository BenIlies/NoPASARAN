import struct
from typing import Iterable
from hpack import Decoder, Encoder
from h2.errors import ErrorCodes
from h2.events import PriorityUpdated, StreamReset, WindowUpdated, DataReceived
from h2.exceptions import FlowControlError, FrameDataMissingError, NoSuchStreamError, ProtocolError, StreamClosedError
from h2.frame_buffer import CONTINUATION_BACKLOG, FrameBuffer
from h2.settings import Settings, SettingCodes
from h2 import settings
from h2.config import H2Configuration, DummyLogger
from h2.connection import AllowedStreamIDs, ConnectionInputs, H2Connection, H2ConnectionStateMachine, _decode_headers, ConnectionState
from h2.stream import H2Stream, StreamClosedBy, StreamInputs
from hyperframe.frame import (Frame, RstStreamFrame, HeadersFrame, PushPromiseFrame, SettingsFrame, 
                              DataFrame, WindowUpdateFrame, PingFrame, RstStreamFrame, 
                              PriorityFrame, GoAwayFrame, ContinuationFrame, AltSvcFrame, 
                              ExtensionFrame, _STRUCT_HL, _STRUCT_L)
from hyperframe.exceptions import InvalidFrameError, InvalidDataError, InvalidPaddingError
from hyperframe.flags import Flags
from h2.utilities import SizeLimitDict
from h2.windows import WindowManager
from h2 import utilities
from typing import Optional, Tuple, List

def redefine_methods(cls, methods_dict):
    for method_name, new_method in methods_dict.items():
        setattr(cls, method_name, new_method)
        
def new_validate_setting(setting, value):  # noqa: C901
    """
    Confirms that a specific setting has a well-formed value. If the setting is
    invalid, returns an error code. Otherwise, returns 0 (NO_ERROR).
    """

    return 0

def H2Configuration__init__(self,
                client_side=True,
                header_encoding=None,
                validate_outbound_headers=True,
                normalize_outbound_headers=True,
                split_outbound_cookies=False,
                validate_inbound_headers=True,
                normalize_inbound_headers=True,
                logger=None,
                skip_initial_settings=False,
                skip_initial_settings_ack=False,
                incorrect_client_connection_preface=False,
                skip_client_connection_preface=False):
    self.client_side = client_side
    self.header_encoding = header_encoding
    self.validate_outbound_headers = validate_outbound_headers
    self.normalize_outbound_headers = normalize_outbound_headers
    self.split_outbound_cookies = split_outbound_cookies
    self.validate_inbound_headers = validate_inbound_headers
    self.normalize_inbound_headers = normalize_inbound_headers
    self.logger = logger or DummyLogger(__name__)
    self.skip_initial_settings = skip_initial_settings
    self.skip_initial_settings_ack = skip_initial_settings_ack
    self.incorrect_client_connection_preface = incorrect_client_connection_preface
    self.skip_client_connection_preface = skip_client_connection_preface

class H2ConnectionStateMachineOverride(H2ConnectionStateMachine):
    """Override the state machine to allow DATA frames in IDLE state"""
    
    def __init__(self):
        super().__init__()
    
    def process_input(self, input_: ConnectionInputs) -> List[str]:
        """
        Override the process_input method to allow DATA frames in IDLE state
        """
        # If we're in IDLE state and trying to send or receive data, just allow it
        if (self.state == ConnectionState.IDLE and 
            input_ in (ConnectionInputs.SEND_DATA, ConnectionInputs.RECV_DATA, 
                      ConnectionInputs.SEND_HEADERS, ConnectionInputs.RECV_HEADERS,
                      ConnectionInputs.RECV_RST_STREAM, ConnectionInputs.RECV_PUSH_PROMISE)):
            return []

        # Otherwise, use the original logic
        return super().process_input(input_)

def H2Connection__init__modified(self, config=None):
    """Modified init that uses our custom state machine"""
    self.state_machine = H2ConnectionStateMachineOverride()
    self.streams = {}
    self.highest_inbound_stream_id = 0
    self.highest_outbound_stream_id = 0
    self.encoder = Encoder()
    self.decoder = Decoder()

    # This won't always actually do anything: for versions of HPACK older
    # than 2.3.0 it does nothing. However, we have to try!
    self.decoder.max_header_list_size = self.DEFAULT_MAX_HEADER_LIST_SIZE

    #: The configuration for this HTTP/2 connection object.
    #:
    #: .. versionadded:: 2.5.0
    self.config = config
    if self.config is None:
        self.config = H2Configuration(
            client_side=True,
        )

    # Objects that store settings, including defaults.
    self.local_settings = Settings(
        client=self.config.client_side,
        initial_values={
            SettingCodes.MAX_CONCURRENT_STREAMS: 100,
            SettingCodes.MAX_HEADER_LIST_SIZE:
                self.DEFAULT_MAX_HEADER_LIST_SIZE,
        }
    )
    self.remote_settings = Settings(client=not self.config.client_side)

    # The current value of the connection flow control windows on the
    # connection.
    self.outbound_flow_control_window = (
        self.remote_settings.initial_window_size
    )

    #: The maximum size of a frame that can be emitted by this peer, in
    #: bytes.
    self.max_outbound_frame_size = self.remote_settings.max_frame_size

    #: The maximum size of a frame that can be received by this peer, in
    #: bytes.
    self.max_inbound_frame_size = self.local_settings.max_frame_size

    # Buffer for incoming data.
    self.incoming_buffer = FrameBuffer(server=not self.config.client_side, skip_client_connection_preface=self.config.skip_client_connection_preface)

    # A private variable to store a sequence of received header frames
    # until completion.
    self._header_frames = []

    # Data that needs to be sent.
    self._data_to_send = bytearray()

    # Keeps track of how streams are closed.
    self._closed_streams = SizeLimitDict(
        size_limit=self.MAX_CLOSED_STREAMS
    )

    # The flow control window manager for the connection.
    self._inbound_flow_control_window_manager = WindowManager(
        max_window_size=self.local_settings.initial_window_size
    )

    # When in doubt use dict-dispatch.
    self._frame_dispatch_table = {
        HeadersFrame: self._receive_headers_frame,
        PushPromiseFrame: self._receive_push_promise_frame,
        SettingsFrame: self._receive_settings_frame,
        DataFrame: self._receive_data_frame,
        WindowUpdateFrame: self._receive_window_update_frame,
        PingFrame: self._receive_ping_frame,
        RstStreamFrame: self._receive_rst_stream_frame,
        PriorityFrame: self._receive_priority_frame,
        GoAwayFrame: self._receive_goaway_frame,
        ContinuationFrame: self._receive_naked_continuation,
        AltSvcFrame: self._receive_alt_svc_frame,
        ExtensionFrame: self._receive_unknown_frame
    }

def new_initiate_connection(self):
    """
    Provides any data that needs to be sent at the start of the connection.
    Must be called for both clients and servers.
    """
    self.config.logger.debug("Initializing connection")

    if self.config.skip_client_connection_preface:
        return
    
    # Only process SEND_SETTINGS if we're not skipping settings
    if not self.config.skip_initial_settings:
        self.state_machine.process_input(ConnectionInputs.SEND_SETTINGS)
    
    if self.config.client_side:
        if self.config.incorrect_client_connection_preface:
            preamble = b'PRI * HTTP/1.1\r\n\r\nSM\r\n\r\n'
        else:
            preamble = b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n'
    else:
        preamble = b''

    # Only send SETTINGS frame if we're not skipping it
    if not self.config.skip_initial_settings:
        f = SettingsFrame(0)
        for setting, value in self.local_settings.items():
            f.settings[setting] = value
        self._data_to_send += preamble + f.serialize()
    else:
        self._data_to_send += preamble

def new_begin_new_stream(self, stream_id, allowed_ids):
    """
    Initiate a new stream.

    .. versionchanged:: 2.0.0
        Removed this function from the public API.

    :param stream_id: The ID of the stream to open.
    :param allowed_ids: What kind of stream ID is allowed.
    """
    self.config.logger.debug(
        "Attempting to initiate stream ID %d", stream_id
    )
    outbound = self._stream_id_is_outbound(stream_id)

    s = H2Stream(
        stream_id,
        config=self.config,
        inbound_window_size=self.local_settings.initial_window_size,
        outbound_window_size=self.remote_settings.initial_window_size
    )
    self.config.logger.debug("Stream ID %d created", stream_id)
    s.max_inbound_frame_size = self.max_inbound_frame_size
    s.max_outbound_frame_size = self.max_outbound_frame_size

    self.streams[stream_id] = s
    self.config.logger.debug("Current streams: %s", self.streams.keys())

    if outbound:
        self.highest_outbound_stream_id = stream_id
    else:
        self.highest_inbound_stream_id = stream_id

    return s

def new_receive_push_promise_frame(self, frame):
    """
    Receive a push-promise frame on the connection.
    If we're a server, convert it to a HEADERS frame.
    """
    # If we're a server, convert PUSH_PROMISE to HEADERS
    if not self.config.client_side:
        # Create headers frame with same data
        headers_frame = HeadersFrame(frame.stream_id)
        headers_frame.data = frame.data
        headers_frame.flags = frame.flags
        headers_frame.pad_length = frame.pad_length
        
        # Process as headers frame
        return self._receive_headers_frame(headers_frame)

    # Original PUSH_PROMISE handling for clients
    pushed_headers = _decode_headers(self.decoder, frame.data)
    events = []

    try:
        if frame.stream_id == 0:
            stream = self._get_stream_by_id(1)
        else:
            stream = self._get_stream_by_id(frame.stream_id)
    except NoSuchStreamError:
        if (self._stream_closed_by(frame.stream_id) ==
                StreamClosedBy.SEND_RST_STREAM):
            f = RstStreamFrame(frame.promised_stream_id)
            f.error_code = ErrorCodes.REFUSED_STREAM
            return [f], events
        raise ProtocolError("Attempted to push on closed stream.")

    try:
        frames, stream_events = stream.receive_push_promise_in_band(
            frame.promised_stream_id,
            pushed_headers,
            self.config.header_encoding,
        )
    except StreamClosedError:
        f = RstStreamFrame(frame.promised_stream_id)
        f.error_code = ErrorCodes.REFUSED_STREAM
        return [f], events

    new_stream = self._begin_new_stream(
        frame.promised_stream_id, AllowedStreamIDs.EVEN
    )
    self.streams[frame.promised_stream_id] = new_stream
    new_stream.remotely_pushed(pushed_headers)

    return frames, events + stream_events
    
def new_receive_priority_frame(self, frame):
    """
    Receive a PRIORITY frame on the connection.
    """
    events = self.state_machine.process_input(
        ConnectionInputs.RECV_PRIORITY
    )

    event = PriorityUpdated()
    event.stream_id = frame.stream_id
    event.depends_on = frame.depends_on
    event.exclusive = frame.exclusive

    # Weight is an integer between 1 and 256, but the byte only allows
    # 0 to 255: add one.
    event.weight = frame.stream_weight + 1

    events.append(event)

    return [], events

def new_receive_rst_stream_frame(self, frame):
    """
    Receive a RST_STREAM frame on the connection.
    Allow continued frame processing after reset.
    """
    # Skip state machine validation for RST_STREAM
    # events = self.state_machine.process_input(
    #     ConnectionInputs.RECV_RST_STREAM
    # )
    stream_events = []
    
    if frame.stream_id == 0:
        event = StreamReset()
        event.stream_id = 0
        stream_events.append(event)
        stream_frames = []
    else:
        # Don't remove the stream from self.streams after reset
        # stream = self._get_stream_by_id(frame.stream_id)
        
        # Create reset event but don't close stream
        event = StreamReset()
        event.stream_id = frame.stream_id
        stream_events.append(event)
        stream_frames = []

    return stream_frames, stream_events

def FrameBuffer__init__(self, server=False, skip_client_connection_preface=False):
    self.data = b''
    self.max_frame_size = 0
    self._preamble = b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n' if server else b''
    self._preamble_len = 0 if skip_client_connection_preface else len(self._preamble)
    self._headers_buffer = []

def new_add_data(self, data):
    """
    Add more data to the frame buffer.

    :param data: A bytestring containing the byte buffer.
    """
    if self._preamble_len:
        data_len = len(data)
        of_which_preamble = min(self._preamble_len, data_len)

        data = data[of_which_preamble:]
        self._preamble_len -= of_which_preamble
        self._preamble = self._preamble[of_which_preamble:]

    self.data += data

def new__next__(self):
    """Modified __next__ to convert CONTINUATION frames to independent HEADERS frames"""
    if len(self.data) < 9:
        raise StopIteration()

    try:
        frame_type = self.data[3]
        stream_id = int.from_bytes(self.data[5:9], byteorder='big') & 0x7FFFFFFF
        
        # If it's a CONTINUATION frame, convert to HEADERS frame
        if frame_type == 0x9:  # CONTINUATION frame type
            new_data = bytearray(self.data)
            new_data[3] = 0x1  # Change to HEADERS frame type
            
            # Ensure each CONTINUATION is treated as an independent HEADERS frame
            # by setting appropriate flags
            flags = new_data[4]
            if flags & 0x4:  # END_HEADERS flag
                new_data[4] = flags | 0x4  # Keep END_HEADERS
            else:
                new_data[4] = flags & ~0x4  # Remove END_HEADERS
                
            self.data = bytes(new_data)
        
        f, length = Frame.parse_frame_header(self.data[:9])
    except (InvalidDataError, InvalidFrameError) as e:
        raise ProtocolError(
            "Received frame with invalid header: %s" % str(e)
        )

    if len(self.data) < length + 9:
        raise StopIteration()

    try:
        f.parse_body(memoryview(self.data[9:9+length]))
    except InvalidDataError:
        raise ProtocolError("Received frame with non-compliant data")
    except InvalidFrameError:
        raise FrameDataMissingError("Frame data missing or invalid")

    self.data = self.data[9+length:]
    return f

def Frame__init__(self, stream_id: int, flags: Iterable[str] = ()):
    #: The stream identifier for the stream this frame was received on.
    #: Set to 0 for frames sent on the connection (stream-id 0).
    self.stream_id = stream_id

    #: The flags set for this frame.
    self.flags = Flags(self.defined_flags)

    #: The frame length, excluding the nine-byte header.
    self.body_len = 0

    for flag in flags:
        self.flags.add(flag)

def new_rststream_parse_body(self, data: memoryview):
    try:
        self.error_code = 0
    except struct.error:  # pragma: no cover
        raise InvalidFrameError("Invalid RST_STREAM body")

    self.body_len = 4

def new_settings_parse_body(self, data: memoryview):
    body_len = len(data)
    for i in range(0, (len(data) // 6) * 6, 6):
        try:
            name, value = _STRUCT_HL.unpack(data[i:i+6])
        except struct.error:
            raise InvalidFrameError("Invalid SETTINGS body")

        self.settings[name] = value
        # body_len += 6

    self.body_len = body_len

def new_push_promise_parse_body(self, data: memoryview):
    padding_data_length = self.parse_padding_data(data)

    try:
        self.promised_stream_id = _STRUCT_L.unpack(
            data[padding_data_length:padding_data_length + 4]
        )[0]
    except struct.error:
        raise InvalidFrameError("Invalid PUSH_PROMISE body")

    self.data = (
        data[padding_data_length + 4:len(data)-self.pad_length].tobytes()
    )
    self.body_len = len(data)

    if self.pad_length and self.pad_length >= self.body_len:
        raise InvalidPaddingError("Padding is too long.")


def new_window_update_parse_body(self, data: memoryview) -> None:
    try:
        self.window_increment = _STRUCT_L.unpack(data)[0]
    except struct.error:
        raise InvalidFrameError("Invalid WINDOW_UPDATE body")

    self.body_len = 4

def new_receive_window_update_frame(self, frame):
    """
    Receive a WINDOW_UPDATE frame on the connection.
    """
    # hyperframe will take care of validating the window_increment.
    # If we reach in here, we can assume a valid value.

    events = self.state_machine.process_input(
        ConnectionInputs.RECV_WINDOW_UPDATE
    )

    if frame.stream_id:
        try:
            stream = self._get_stream_by_id(frame.stream_id)
            frames, stream_events = stream.receive_window_update(
                frame.window_increment
            )
        except StreamClosedError:
            return [], events
    else:
        # Increment our local flow control window.
        self.outbound_flow_control_window = self.outbound_flow_control_window + frame.window_increment

        # FIXME: Should we split this into one event per active stream?
        window_updated_event = WindowUpdated()
        window_updated_event.stream_id = 0
        window_updated_event.delta = frame.window_increment
        stream_events = [window_updated_event]
        frames = []

    return frames, events + stream_events


def new_update_header_buffer(self, f):
    """Simplified header buffer that just passes frames through"""
    if isinstance(f, ContinuationFrame):
        # Convert CONTINUATION to HEADERS frame to process it independently
        headers_frame = HeadersFrame(f.stream_id)
        headers_frame.data = f.data
        headers_frame.flags = f.flags
        return headers_frame
    
    return f

def new_send_data(self, stream_id, data, end_stream=False, pad_length=None):
    """
    Modified send_data to force sending DATA frames even in IDLE state
    """
    self.config.logger.debug(
        "Send data on stream ID %d with len %d", stream_id, len(data)
    )
    
    frame_size = len(data)
    if pad_length is not None:
        if not isinstance(pad_length, int):
            raise TypeError("pad_length must be an int")
        if pad_length < 0 or pad_length > 255:
            raise ValueError("pad_length must be within range: [0, 255]")
        frame_size += pad_length + 1

    # Create and send DATA frame directly
    df = DataFrame(stream_id)
    df.data = data
    if end_stream:
        df.flags.add('END_STREAM')
    if pad_length is not None:
        df.flags.add('PADDED')
        df.pad_length = pad_length

    # Serialize the frame and add it to the output buffer
    self._data_to_send += df.serialize()
    
    # Update flow control window
    self.outbound_flow_control_window -= frame_size
    self.config.logger.debug(
        "Outbound flow control window size is %d",
        self.outbound_flow_control_window
    )
    
    return

def new_receive_naked_continuation(self, frame):
    """
    A CONTINUATION frame has been received. This is only valid if we're already
    in the middle of receiving headers.
    """
    # If we're not in the middle of receiving headers, this is a problem.
    if not self._header_frames:
        # Skip triggering the error by ignoring the frame
        return [], []
        # Original error code:
        # return self._receive_naked_continuation(frame)

    # Otherwise, keep receiving headers.
    self._header_frames.append(frame)
    
    if 'END_HEADERS' in frame.flags:
        # End of headers, process them.
        headers = _decode_headers(
            self.decoder,
            b''.join(f.data for f in self._header_frames)
        )
        # Preserve first before clearing
        first = self._header_frames[0]
        self._header_frames = []
        
        # Process according to the type of the first frame.
        if isinstance(first, HeadersFrame):
            return self._receive_headers(first, headers)
        elif isinstance(first, PushPromiseFrame):
            return self._receive_push_promise(first, headers)
        else:
            # This shouldn't happen, but handle it gracefully
            return [], []
    
    return [], []

def new_receive_data_frame(self, frame):
    """
    Modified _receive_data_frame to handle DATA frames in any state
    """
    # Don't enforce stream state checks
    flow_controlled_length = len(frame.data) + frame.pad_length + 1 if frame.pad_length else len(frame.data)
    
    # Maintain the flow control window
    self._inbound_flow_control_window_manager.window_consumed(
        flow_controlled_length
    )
    
    # Return the event
    return [], [DataReceived()]

def send_headers(self, headers, encoder, end_stream=False):
    """
    Returns a list of HEADERS/CONTINUATION frames to emit as either headers
    or trailers.
    """
    self.config.logger.debug("Send headers %s on %r", headers, self)

    # Because encoding headers makes an irreversible change to the header
    # compression context, we make the state transition before we encode
    # them.

    # First, check if we're a client. If we are, no problem: if we aren't,
    # we need to scan the header block to see if this is an informational
    # response.
    input_ = StreamInputs.SEND_HEADERS
    if ((not self.state_machine.client) and
            False):
        if end_stream:
            raise ProtocolError(
                "Cannot set END_STREAM on informational responses."
            )

        input_ = StreamInputs.SEND_INFORMATIONAL_HEADERS

    events = self.state_machine.process_input(input_)

    hf = HeadersFrame(self.stream_id)
    hdr_validation_flags = self._build_hdr_validation_flags(events)
    frames = self._build_headers_frames(
        headers, encoder, hf, hdr_validation_flags
    )

    if end_stream:
        # Not a bug: the END_STREAM flag is valid on the initial HEADERS
        # frame, not the CONTINUATION frames that follow.
        self.state_machine.process_input(StreamInputs.SEND_END_STREAM)
        frames[0].flags.add('END_STREAM')

    # if self.state_machine.trailers_sent and not end_stream:
    #     raise ProtocolError("Trailers must have END_STREAM set.")

    # if self.state_machine.client and self._authority is None:
    #     self._authority = authority_from_headers(headers)

    # store request method for _initialize_content_length
    # self.request_method = extract_method_header(headers)

    return frames

def receive_headers(self, headers, end_stream, header_encoding):
    """
    Receive a set of headers (or trailers).
    """
    if False:
        if end_stream:
            raise ProtocolError(
                "Cannot set END_STREAM on informational responses"
            )
        input_ = StreamInputs.RECV_INFORMATIONAL_HEADERS
    else:
        input_ = StreamInputs.RECV_HEADERS

    events = self.state_machine.process_input(input_)

    if end_stream:
        es_events = self.state_machine.process_input(
            StreamInputs.RECV_END_STREAM
        )
        events[0].stream_ended = es_events[0]
        events += es_events

    self._initialize_content_length(headers)

    # if isinstance(events[0], TrailersReceived):
    #     if not end_stream:
    #         raise ProtocolError("Trailers must have END_STREAM set")

    hdr_validation_flags = self._build_hdr_validation_flags(events)
    events[0].headers = self._process_received_headers(
        headers, hdr_validation_flags, header_encoding
    )
    return [], events

redefine_methods(settings, {'_validate_setting': new_validate_setting})
redefine_methods(H2Configuration, {'__init__': H2Configuration__init__})
redefine_methods(H2Connection, {
    '__init__': H2Connection__init__modified,
    '_begin_new_stream': new_begin_new_stream,
    '_receive_push_promise_frame': new_receive_push_promise_frame,
    '_receive_priority_frame': new_receive_priority_frame,
    'initiate_connection': new_initiate_connection,
    '_receive_rst_stream_frame': new_receive_rst_stream_frame,
    '_receive_window_update_frame': new_receive_window_update_frame,
    'send_data': new_send_data,
    '_receive_data_frame': new_receive_data_frame,
    '_receive_naked_continuation': new_receive_naked_continuation
})
redefine_methods(FrameBuffer, {
    '__init__': FrameBuffer__init__, 
    'add_data': new_add_data, 
    '__next__': new__next__, 
    '_update_header_buffer': new_update_header_buffer
})
redefine_methods(Frame, {'__init__': Frame__init__})
redefine_methods(RstStreamFrame, {'parse_body': new_rststream_parse_body})
redefine_methods(SettingsFrame, {'parse_body': new_settings_parse_body})
redefine_methods(PushPromiseFrame, {'parse_body': new_push_promise_parse_body})
redefine_methods(WindowUpdateFrame, {'parse_body': new_window_update_parse_body})
redefine_methods(H2Stream, {'receive_headers': receive_headers, 'send_headers': send_headers})