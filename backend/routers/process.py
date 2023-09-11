from fastapi import FastAPI, UploadFile, HTTPException
from services.process import DataService

app = FastAPI()


@app.post("/upload_xml")
async def upload_xml(file: UploadFile):
    # xml_content = await file.read()
    # payouts = parse_xml(xml_content)

    # save_payouts_to_db(payouts)

    return {"status": "success"}


@app.post("/make_payments")
def make_payments():
    # all_payouts = payouts_collection.find({})
    # for payout in all_payouts:
    #     make_payment(Payout(**payout))

    return {"status": "payments made"}
