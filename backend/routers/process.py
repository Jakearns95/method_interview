from fastapi import FastAPI, HTTPException, Response, status
from utils.formating import convert_to_csv
from pydantic import BaseModel

import csv
from io import StringIO, BytesIO
from services.process import DataService
from utils.routing import public_router
import zipfile

app = FastAPI()
public_router = public_router(tags=["process"])


class XMLPayload(BaseModel):
    payload: str


@public_router.post("/upload_xml")
def upload_xml(data: XMLPayload):
    try:
        print(data)
        payments = DataService().process_xml(data.payload)

        # TODO: create builder for json api spec responses
        return payments
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@public_router.post("/authorize_payments/{batch_id}")
def authorize_payments(
    batch_id: str,
):
    try:
        DataService().process_payments_for_batch(batch_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@public_router.get("/batch_files")
def get_batch_files():
    try:
        batch_records = DataService().get_all_batch_records()
        return batch_records
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@public_router.get("/batch_report/{batch_id}")
def get_batch_report(batch_id: str):
    try:
        data_service = DataService()

        get_payments = data_service.get_all_payments(batch_id)
        get_total_by_branch = data_service.get_total_by_branch(batch_id)
        get_total_by_corp = data_service.get_total_by_corp(batch_id)

        # Convert the data lists to CSV strings using the helper function
        output1 = convert_to_csv(get_payments)
        output2 = convert_to_csv(get_total_by_branch)
        output3 = convert_to_csv(get_total_by_corp)

        # Create a zip of the CSVs
        zip_output = BytesIO()
        with zipfile.ZipFile(zip_output, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("data1.csv", output1.getvalue())
            zf.writestr("data2.csv", output2.getvalue())
            zf.writestr("data3.csv", output3.getvalue())

        zip_output.seek(0)
        return Response(
            content=zip_output.read(),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={batch_id}.zip"},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
