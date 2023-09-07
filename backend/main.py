from dotenv import find_dotenv, load_dotenv

# place at top so env vars cascade to all imports below
load_dotenv(find_dotenv(".env.localdev"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from routers import users
import os


DB_URL = os.environ.get("DB_URL")
DB_NAME = os.environ.get("DB_NAME")

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_origins="http://localhost:3000,http://127.0.0.1:3000",
    allow_origin_regex="",
)


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(users.public_router)


@app.get("/")
def root_smoke_test():
    return {"status": "OK"}
