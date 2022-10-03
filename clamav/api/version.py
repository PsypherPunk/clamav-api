import anyio
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
    async with await anyio.connect_unix("/var/run/clamav/clamd.ctl") as stream:
        await stream.send(b"VERSION\n")
        output = await stream.receive(4096)

    return Output(output=output.decode("utf-8").strip())
