from fastapi import Depends, HTTPException


from utils.logging import init_logger
from utils.routing import public_router

public_router = public_router(tags=["countries"])

logger = init_logger(__name__)


@public_router.get("/")
def get():
    """ """
    try:
        return "Test"
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500)
