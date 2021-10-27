from io import BytesIO
import logging
import base64
import os
import json

import azure.functions as func
from pdfcompare import pdfcompare_module

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    pdfOld = ""
    pdfNew = ""

    try:
        req_body = req.get_json()
        pdfOld = req_body.get("pdfOld")
        pdfNew = req_body.get("pdfNew")
    except ValueError:
        return func.HttpResponse("Request body is not valid JSON", status_code=400)

    if not pdfOld or not pdfNew:
        return func.HttpResponse(
            "One or more parameters missing. Required: pdfOld, pdfNew.",
            status_code=400
        )
    
    script_dir = os.path.dirname(__file__)
    pdf_path_old = os.path.join(script_dir, "pdf_old.pdf")
    pdf_path_new = os.path.join(script_dir, 'pdf_new.pdf')

    # Write both input pdf files to the current directory,
    # since pdftohtml uses them via subprocess.
    # We need to strip the base64 header at ',' before writing the file.
    with open(pdf_path_old,"wb") as f:
        f.write(base64.b64decode(pdfOld.split(",", 1)[-1]))
    with open(pdf_path_new,"wb") as f:
        f.write(base64.b64decode(pdfNew.split(",", 1)[-1]))

    base64String = ''
    hits = 0

    try:
        (output, hits) = pdfcompare_module.compare_pdfs(pdf_path_old, pdf_path_new)
        out = BytesIO()
        output.write(out)
        base64String = "data:image/pdf;base64," + base64.b64encode(out.getvalue()).decode()
    except Exception as e:
        logging.exception(e)
    except SystemExit as e: # Catch parser.exit()
        logging.exception(e)
    finally:
        if os.path.exists(pdf_path_old):
            os.remove(pdf_path_old)
        if os.path.exists(pdf_path_new):
            os.remove(pdf_path_new)

    if base64String:
        return func.HttpResponse(json.dumps({
            "changePdf": base64String,
            "hasChanges": hits > 0
        }), mimetype="application/json", status_code=200)

    return func.HttpResponse(
        "No PDF was generated, check the logs for details",
        status_code=500
    )
