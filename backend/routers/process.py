import json

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

from services.process import DataService
from utils.routing import public_router

app = FastAPI()
public_router = public_router(tags=["process"])


class XMLPayload(BaseModel):
    data: str


@public_router.post("/upload_xml")
def upload_xml(payload: XMLPayload):
    try:
        payments = DataService().process_xml(payload.data)

        # TODO: create builder for json api spec responses
        return payments
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@public_router.post("/authorize_payments")
def authorize_payments(
    batch_id: str,
):
    try:
        DataService().process_payments_for_batch(batch_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
