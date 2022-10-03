import anyio
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
    async with await anyio.connect_unix("/var/run/clamav/clamd.ctl") as stream:
        await stream.send(b"PING\n")
        output = await stream.receive(4096)

    return Output(output=output.decode("utf-8").strip())
