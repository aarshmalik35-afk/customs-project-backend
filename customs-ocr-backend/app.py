from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

import os
import uuid
import base64

from ocr import run_ocr
from extract_fields import extract_fields


# =========================================================
# BASE64 REQUEST MODEL
# =========================================================

class InvoiceBase64Request(BaseModel):
    filename: str
    image_base64: str


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Customs OCR Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aarshmalik35-afk.github.io"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# FOLDERS
# =========================================================

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "status": "online",
        "service": "Customs OCR Backend"
    }


# =========================================================
# ORIGINAL FILE UPLOAD ENDPOINT
# =========================================================

@app.post("/process-invoice")
async def process_invoice(
    file: UploadFile = File(...)
):

    try:

        # Generate unique filename
        file_id = str(uuid.uuid4())

        extension = os.path.splitext(
            file.filename
        )[1]

        if not extension:
            extension = ".jpg"

        image_path = os.path.join(
            UPLOAD_FOLDER,
            file_id + extension
        )

        output_path = os.path.join(
            OUTPUT_FOLDER,
            file_id + "_ocr.txt"
        )

        # Save uploaded image
        contents = await file.read()

        with open(
            image_path,
            "wb"
        ) as f:

            f.write(contents)

        # Run OCR
        ocr_text = run_ocr(
            image_path,
            output_path
        )

        # Extract fields + risk
        data = extract_fields(
            ocr_text
        )

        return {
            "success": True,
            "filename": file.filename,
            "data": data
        }

    except Exception as e:

        print("ERROR:", e)

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# BASE64 ENDPOINT FOR POWER APPS
# =========================================================

@app.post("/process-invoice-base64")
async def process_invoice_base64(
    request: InvoiceBase64Request
):

    try:

        print("\n================================")
        print("BASE64 INVOICE RECEIVED")
        print("================================")

        print(
            "Filename:",
            request.filename
        )

        # -------------------------------------------------
        # Remove data URI prefix
        # -------------------------------------------------

        image_data = request.image_base64

        if "," in image_data:

            image_data = image_data.split(
                ",",
                1
            )[1]

        # -------------------------------------------------
        # Decode Base64
        # -------------------------------------------------

        image_bytes = base64.b64decode(
            image_data
        )

        # -------------------------------------------------
        # Generate unique filename
        # -------------------------------------------------

        file_id = str(
            uuid.uuid4()
        )

        extension = os.path.splitext(
            request.filename
        )[1]

        if not extension:

            extension = ".jpg"

        image_path = os.path.join(
            UPLOAD_FOLDER,
            file_id + extension
        )

        output_path = os.path.join(
            OUTPUT_FOLDER,
            file_id + "_ocr.txt"
        )

        # -------------------------------------------------
        # Save image
        # -------------------------------------------------

        with open(
            image_path,
            "wb"
        ) as f:

            f.write(image_bytes)

        print(
            "Image saved:",
            image_path
        )

        # -------------------------------------------------
        # Run OCR
        # -------------------------------------------------

        print("Running OCR...")

        ocr_text = run_ocr(
            image_path,
            output_path
        )

        # -------------------------------------------------
        # Extract fields + risk
        # -------------------------------------------------

        print(
            "Running field extraction..."
        )

        data = extract_fields(
            ocr_text
        )

        print(
            "Processing completed."
        )

        # -------------------------------------------------
        # Return result
        # -------------------------------------------------

        return {

            "success": True,

            "filename": request.filename,

            "data": data

        }

    except Exception as e:

        print(
            "\nBASE64 PROCESSING ERROR:",
            e
        )

        return {

            "success": False,

            "error": str(e)

        }
