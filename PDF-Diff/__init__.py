from io import BytesIO
import logging
import base64
import os
import sys
from PyPDF2.generic import NullObject

import azure.functions as func
import pdfcompare.pdfcompare

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    pdf1 = ""
    pdf2 = ""

    try:
        req_body = req.get_json()
        pdf1 = req_body.get("pdf1")
        pdf2 = req_body.get("pdf2")
    except ValueError:
        return func.HttpResponse("Request body is not valid JSON", status_code=400)

    if pdf1.__len__() == 0 or pdf2.__len__() == 0:
        return func.HttpResponse(
            "One or more parameters missing. Required: pdf1, pdf2.",
            status_code=400
        )
    

    script_dir = os.path.dirname(__file__)
    test_pdf_path_old = os.path.join(script_dir, 'E4N_Exam_1.pdf')
    test_pdf_path_new = os.path.join(script_dir, 'E4N_Exam_1_1.pdf')

    saved_argv = sys.argv
    base64String = ''

    try:
        sys.argv = [
            '-c',
            test_pdf_path_old,
            test_pdf_path_new,
        ]
        output = pdfcompare.pdfcompare.main()
        out = BytesIO()
        output.write(out)
        base64String = "data:image/pdf;base64," + base64.b64encode(out.getvalue()).decode()
    except Exception as e:
        logging.exception(e)
    finally:
        sys.argv = saved_argv

    if base64String.__len__() > 0:
        return func.HttpResponse(base64String)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
