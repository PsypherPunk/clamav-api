import socket
import struct

from fastapi import APIRouter, Body

from clamav.models import Output

router = APIRouter()


@router.post(
    path="/instream",
    description="""It is mandatory to prefix this command with n or z.

Scan a stream of data. The stream is sent to clamd in chunks, after
INSTREAM, on the same socket on which the command was sent. This avoids
the overhead of establishing new TCP connections and problems with NAT.
The format of the chunk is: '<length><data>' where <length> is the size
of the following data in bytes expressed as a 4 byte unsigned integer
in network byte order and <data> is the actual chunk. Streaming is
terminated by sending a zero-length chunk. Note: do not exceed
StreamMaxLength as defined in clamd.conf, otherwise clamd will reply
with INSTREAM size limit exceeded and close the connection.""",
    summary="Scan a stream of data.",
    response_model=Output,
)
def post(body: bytes = Body(...)):
    """
    Scans a stream of data using clamd's ``INSTREAM`` command.

    The command is first prefixed with ``z`` and terminated with the
    null character before being sent.

    The payload (i.e. the data to be scanned) is then sent, prefixed
    by its length. Strictly, the data should be chunked. However, the
    default ``StreamMaxLength`` is 25MB which exceeds the limits of
    this API.

    :param body: binary data to be scanned
    :return: JSON-structured response from clamd
    """
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect("/var/run/clamav/clamd.ctl")

        s.send(b"zINSTREAM\0")

        size = struct.pack(b"!L", len(body))
        s.send(size + body)

        s.send(struct.pack(b"!L", 0))

        output = s.recv(4096)

    return Output(output=output.decode("utf-8").strip())
