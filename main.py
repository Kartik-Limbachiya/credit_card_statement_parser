from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from parser import CreditCardStatementParser
import os
import tempfile
import uvicorn

app = FastAPI(
    title="Credit Card Statement Parser API",
    description="Extracts key info from credit card statements (Axis, BOB, Kotak, SBI)",
    version="1.0.0"
)

parser = CreditCardStatementParser()

@app.post("/parse-statement/")
async def parse_statement(bank: str = Form(...), file: UploadFile = File(...)):
    """
    Upload a PDF and specify the bank (axis, bob, kotak, sbi).
    Example: 
        curl -X POST -F "bank=axis" -F "file=@Axis1-unlocked.pdf" https://yourapi.onrender.com/parse-statement/
    """
    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Parse PDF
        result = parser.parse_statement(tmp_path, bank)

        # Clean up temp file
        os.remove(tmp_path)

        return JSONResponse(content=result.to_dict())

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/")
async def root():
    return {"message": "Welcome to Credit Card Parser API 🚀", "usage": "/parse-statement/"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
