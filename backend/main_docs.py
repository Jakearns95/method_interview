import os
import secrets

from dotenv import find_dotenv, load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from main import app

# Load in ENV variables
load_dotenv(find_dotenv(".env.localdev"))

docs_app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

security = HTTPBasic()


def use_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    basic_auth_username = os.environ.get("FAST_API_DOCS_BASIC_AUTH_USERNAME")
    basic_auth_password = os.environ.get("FAST_API_DOCS_BASIC_AUTH_PASSWORD")

    if basic_auth_username and basic_auth_password:
        is_correct_username: bool = secrets.compare_digest(
            credentials.username, basic_auth_username
        )
        is_correct_password: bool = secrets.compare_digest(
            credentials.password, basic_auth_password
        )
        if not (is_correct_username and is_correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
                headers={"WWW-Authenticate": "Basic"},
            )


@docs_app.get("/docs", include_in_schema=False)
def get_swagger_documentation(username: str = Depends(use_basic_auth)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@docs_app.get("/redoc", include_in_schema=False)
def get_redoc_documentation(username: str = Depends(use_basic_auth)):
    return get_redoc_html(openapi_url="/openapi.json", title="docs")


@docs_app.get("/openapi.json", include_in_schema=False)
def openapi(username: str = Depends(use_basic_auth)):
    return get_openapi(title="openapi", version=app.version, routes=app.routes)
