import socket

from fastapi import APIRouter

from clamav.models import Output

router = APIRouter()


@router.get(
    path="/version",
    description="Print program and database versions.",
    summary="Print program and database versions.",
    response_model=Output,
)
async def version():
    """
    Retrieve program and database versions using clamd's ``VERSION``
    command.

    :return: JSON-structured response from clamd
    """
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect("/var/run/clamav/clamd.ctl")
        s.send(b"nVERSION\n")
        output = s.recv(4096)

    return Output(output=output.decode("utf-8").strip())
