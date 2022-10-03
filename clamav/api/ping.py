import socket

from fastapi import APIRouter

from clamav.models import Output

router = APIRouter()


@router.get(
    path="/ping",
    description='Check the server\'s state. It should reply with "PONG".',
    summary="Check the server's state.",
    response_model=Output,
)
async def ping():
    """
    Check the server's state using clamd's ``PING`` command.

    It should reply with ``PONG``.

    :return: JSON-structured response from clamd
    """
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect("/var/run/clamav/clamd.ctl")
        s.send(b"nPING\n")
        output = s.recv(4096)

    return Output(output=output.decode("utf-8").strip())
