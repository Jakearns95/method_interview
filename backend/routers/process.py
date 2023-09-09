from fastapi import FastAPI, UploadFile, HTTPException
from services.processing import DataService

app = FastAPI()


@app.post("/process-xml/")
async def process_xml_file():
    # if file.filename.endswith(".xml"):
    #     xml_content = await file.read()
    #     try:
    xml_content = """
    <root>
        <row>
            <Employee>
                <DunkinId>EMP-208c8e79-8d85-4914-9a7a-8a899e67c530</DunkinId>
                <DunkinBranch>BRC-5a32e859-e91a-490c-b4f2-bce67695f30c</DunkinBranch>
                <FirstName>Madie</FirstName>
                <LastName>Funk</LastName>
                <DOB>12-13-2000</DOB>
                <PhoneNumber>+16473020450</PhoneNumber>
            </Employee>
            <Payor>
                <DunkinId>CORP-e4025d0e-0491-49ef-8284-2738c2d0a0cf</DunkinId>
                <ABARouting>148386123</ABARouting>
                <AccountNumber>12719660</AccountNumber>
                <Name>Dunkin' Donuts LLC</Name>
                <DBA>Dunkin' Donuts</DBA>
                <EIN>32120240</EIN>
                <Address>
                    <Line1>999 Hayes Lights</Line1>
                    <City>Kerlukemouth</City>
                    <State>IA</State>
                    <Zip>67485</Zip>
                </Address>
            </Payor>
            <Payee>
                <PlaidId>ins_116947</PlaidId>
                <LoanAccountNumber>91400799</LoanAccountNumber>
            </Payee>
            <Amount>$7.03</Amount>
        </row>
    </root>
    """
    DataService.process_xml(xml_content)
    return {
        "status": "success",
        "message": "XML processed and data upserted successfully!",
    }
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=400, detail=f"Failed to process XML: {str(e)}"
    #     )
    # else:
    #     raise HTTPException(status_code=400, detail="Please provide a valid XML file.")
