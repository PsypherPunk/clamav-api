from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from clamav.api import instream, ping, version

app = FastAPI(
    title="ClamAV API",
    description="Implementation of a HTTP API over ClamAV.",
    contact={
        "email": "psypherpunk+github@gmail.com",
    },
)


@app.get("/")
async def redirect_docs():
    return RedirectResponse("/docs")


app.include_router(instream.router)
app.include_router(ping.router)
app.include_router(version.router)
