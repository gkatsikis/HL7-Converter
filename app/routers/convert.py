from fastapi import APIRouter, Request
from app.parser.hl7_parser import hl7_parser
from app.models.hl7_segments import parse_pid
from app.transformer.to_fhir import pid_to_fhir_patient

router = APIRouter()

@router.post("/convert", tags=["Converters"])
async def convert_hl7_to_fhir(request: Request):
    hl7_message = await request.body()
    hl7_message = hl7_message.decode("utf-8")

    parsed_segments = hl7_parser(hl7_message)
    pid_segment = parsed_segments["PID"]
    parsed_pid = parse_pid(pid_segment)
    fhir_message = pid_to_fhir_patient(parsed_pid)

    if request.headers.get("HX-Request"):
        pass
    else:
        return fhir_message
