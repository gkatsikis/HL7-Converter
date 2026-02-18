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
    receiving_applications: Optional[str] = None
    receiving_facility: Optional[str] = None
    message_datetime: str
    security: Optional[str] = None
    message_type: str
    message_control_id: str
    processing_id: str
    version_id: str