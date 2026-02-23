from pydantic import BaseModel
from typing import Optional


class PIDSegment(BaseModel):
    set_id: str
    patient_id_external: Optional[str] = None
    patient_id: str
    patient_alternate_id: Optional[str] = None
    patient_name: str
    mothers_maiden: Optional[str] = None
    date_of_birth: str
    gender: str
    patient_alias: Optional[str] = None
    race: Optional[str] = None
    address: str
    county_code: Optional[str] = None
    home_phone: Optional[str] = None
    business_phone: Optional[str] = None
    language: Optional[str] = None
    marital_status: Optional[str] = None


class MSHSegment(BaseModel):
    field_separator: str
    encoding_chars: str
    sending_application: Optional[str] = None
    sending_facility: Optional[str] = None
    receiving_application: Optional[str] = None
    receiving_facility: Optional[str] = None
    message_datetime: str
    security: Optional[str] = None
    message_type: str
    message_control_id: str
    processing_id: str
    version_id: str


def parse_pid(pid_list: list) -> PIDSegment:
    return PIDSegment(
        set_id=pid_list[1],
        patient_id_external=pid_list[2] or None,
        patient_id=pid_list[3],
        patient_alternate_id=pid_list[4] or None,
        patient_name=pid_list[5],
        mothers_maiden=pid_list[6] or None,
        date_of_birth=pid_list[7],
        gender=pid_list[8],
        patient_alias=pid_list[9] or None,
        race=pid_list[10] or None,
        address=pid_list[11],
        county_code=pid_list[12] or None,
        home_phone=pid_list[13] or None,
        business_phone=pid_list[14] or None,
        language=pid_list[15] or None,
        marital_status=pid_list[16] or None,
    )


def parse_msh(msh_list: list) -> MSHSegment:
    msh_list.insert(1, "|")
    return MSHSegment(
        field_separator=msh_list[1],
        encoding_chars=msh_list[2],
        sending_application=msh_list[3] or None,
        sending_facility=msh_list[4] or None,
        receiving_application=msh_list[5] or None,
        receiving_facility=msh_list[6] or None,
        message_datetime=msh_list[7],
        security=msh_list[8] or None,
        message_type=msh_list[9],
        message_control_id=msh_list[10],
        processing_id=msh_list[11],
        version_id=msh_list[12],
    )
