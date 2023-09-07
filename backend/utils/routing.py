import time
from enum import Enum
from typing import Callable, List, Union

from fastapi import APIRouter, Depends, Request, Response
from fastapi.routing import APIRoute

from utils.logging import init_logger

logger = init_logger(__name__)


def public_router(tags: List[Union[str, Enum]]):
    return APIRouter(route_class=TimedLoggingRouter, tags=tags)


class TimedLoggingRouter(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()

            try:
                request_headers = dict(request.headers.items())
                request_body: bytes = await request.body()

                response: Response = await original_route_handler(request)
                response_headers = dict(response.headers.items())
                response_body: bytes = response.body

                logger.info(
                    f"STARTED {request.method} {request.url.path} FOR {request.client.host}"
                )
                logger.info(f"REQUEST HEADERS {request_headers}")
                logger.info(f"REQUEST {str(request_body)}")
                logger.info(f"RESPONSE HEADERS {str(response_headers)}")
                logger.info(f"RESPONSE {str(response_body)}")
                duration = round((time.time() - before) * 1000, 4)
                logger.info(
                    f"COMPLETED {response.status_code} {request.method} {request.url.path} FOR {request.client.host} IN {duration}ms"
                )
                return response

            except Exception as e:
                duration = round((time.time() - before) * 1000, 4)
                logger.error(f"ERROR IN {duration}ms")
                logger.error(e)
                raise e

        return custom_route_handler


async def get_request_body(request: Request):
    return await request.body()
