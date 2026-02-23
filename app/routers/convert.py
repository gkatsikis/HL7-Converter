from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.parser.hl7_parser import hl7_parser
from app.models.hl7_segments import parse_pid
from app.transformer.to_fhir import pid_to_fhir_patient
import json

router = APIRouter()

@router.post("/convert", tags=["Converters"])
async def convert_hl7_to_fhir(request: Request):
    content_type = request.headers.get("content-type", "")
    is_htmx = request.headers.get("HX-Request")

    if "form" in content_type:
        form = await request.form()
        hl7_message = form["hl7_message"]
    else:
        body = await request.body()
        hl7_message = body.decode("utf-8")

    if not hl7_message.strip():
        if is_htmx:
            return HTMLResponse(content='<div class="error">Please paste an HL7 message first.</div>')
        return JSONResponse(status_code=400, content={"error": "Empty message body"})

    try:
        parsed_segments = hl7_parser(hl7_message)
    except Exception as e:
        if is_htmx:
            return HTMLResponse(content=f'<div class="error">Failed to parse message: {str(e)}</div>')
        return JSONResponse(status_code=400, content={"error": f"Failed to parse message: {str(e)}"})

    if "PID" not in parsed_segments:
        if is_htmx:
            return HTMLResponse(content='<div class="error">Missing PID segment. Make sure your message contains a PID line.</div>')
        return JSONResponse(status_code=400, content={"error": "Missing PID segment"})

    try:
        parsed_pid = parse_pid(parsed_segments["PID"])
        fhir_message = pid_to_fhir_patient(parsed_pid)
    except Exception as e:
        if is_htmx:
            return HTMLResponse(content=f'<div class="error">Failed to convert message: {str(e)}</div>')
        return JSONResponse(status_code=400, content={"error": f"Failed to convert: {str(e)}"})

    if is_htmx:
        fhir_json = json.dumps(fhir_message.model_dump(), indent=2)
        html = f"<pre>{fhir_json}</pre>"
        return HTMLResponse(content=html)
    else:
        return fhir_message