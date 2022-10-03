from fastapi import FastAPI

from clamav.api import instream, ping, version

app = FastAPI(
    title="ClamAV API",
    description="Implementation of a HTTP API over ClamAV.",
    contact={
        "email": "psypherpunk+github@gmail.com",
    },
    docs_url="/doc",
    redoc_url="/redoc",
)

app.include_router(instream.router, prefix="/v1")
app.include_router(ping.router, prefix="/v1")
app.include_router(version.router, prefix="/v1")
