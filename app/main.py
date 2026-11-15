from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI(
    title="ClassroomLink",
    description=(
        "A local network-based interactive classroom "
        "screen-sharing and laboratory streaming system."
    ),
    version="0.1.0",
)


@app.get("/", response_class=HTMLResponse, tags=["General"])
async def home() -> HTMLResponse:
    return HTMLResponse(
        content="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">
            <title>ClassroomLink</title>
        </head>
        <body>
            <h1>ClassroomLink</h1>
            <p>
                Your local classroom streaming platform
                is starting successfully.
            </p>
        </body>
        </html>
        """
    )


@app.get("/health", tags=["General"])
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "application": "ClassroomLink",
        "version": "0.1.0",
    }