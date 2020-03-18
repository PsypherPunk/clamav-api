import socket
import struct


def post(body):
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
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/var/run/clamav/clamd.ctl")

    s.send(b"zINSTREAM\0")

    size = struct.pack(b"!L", len(body))
    s.send(size + body)

    s.send(struct.pack(b"!L", 0))

    output = s.recv(4096)
    s.close()

    return {
        "output": output.decode("utf-8").strip(),
    }
