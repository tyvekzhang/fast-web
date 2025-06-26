"""Project health probe"""

from fastapi import APIRouter

from src.main.app.core.schema import HttpResponse

probe_router = APIRouter()


@probe_router.get("/liveness")
async def liveness() -> HttpResponse[str]:
    """
    Check if the system is alive.

    Returns:
        HttpResponse[str]: An HTTP response containing a success message
        with the string "Hi".
    """
    return HttpResponse.success(msg="Hi")
