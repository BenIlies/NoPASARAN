from h2.stream import H2Stream, _decode_headers
from hyperframe.frame import ContinuationFrame

def redefine_methods(cls, methods_dict):
    for method_name, new_method in methods_dict.items():
        setattr(cls, method_name, new_method)

def new_process_received_headers(self,
                                headers,
                                header_validation_flags,
                                header_encoding):

    if header_encoding:
        headers = _decode_headers(headers, header_encoding)

    return list(headers)

def new_build_headers_frames(self,
                            headers,
                            encoder,
                            first_frame,
                            hdr_validation_flags):

    encoded_headers = encoder.encode(headers)

    header_blocks = [
        encoded_headers[i:i+self.max_outbound_frame_size]
        for i in range(
            0, len(encoded_headers), self.max_outbound_frame_size
        )
    ]

    frames = []
    first_frame.data = header_blocks[0]
    frames.append(first_frame)

    for block in header_blocks[1:]:
        cf = ContinuationFrame(self.stream_id)
        cf.data = block
        frames.append(cf)

    frames[-1].flags.add('END_HEADERS')
    return frames

redefine_methods(
    H2Stream, 
    {
        '_process_received_headers': new_process_received_headers,
        '_build_headers_frames': new_build_headers_frames,
    }
)