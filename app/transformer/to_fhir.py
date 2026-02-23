from app.models.hl7_segments import parse_pid, PIDSegment
from app.models.fhir_resources import (
    Patient,
    HumanName,
    Address,
    Communication,
    Telecom,
    Identifier,
    Reference,
    CodeableConcept,
    Coding,
)


def convert_gender(hl7_gender: str) -> str:
    gender_map = {
        "M": "male",
        "F": "female",
        "O": "other",
        "U": "unknown",
        "A": "other",
        "N": "other",
    }

    return gender_map.get(hl7_gender, "unknown")


def convert_dob(hl7_dob: str) -> str:
    year = hl7_dob[0:4]
    month = hl7_dob[4:6]
    day = hl7_dob[6:8]

    return f"{year}-{month}-{day}"


def convert_name(hl7_name: str) -> HumanName:
    parts = hl7_name.split("^")
    return HumanName(
        use="official",
        family=parts[0],
        given=parts[1:],
    )

def convert_address(hl7_address: str) -> Address:
    parts = hl7_address.split("^")
    return Address(
        use="home",
        line=[parts[0]],
        city=parts[2],
        state=parts[3],
        postalCode=parts[4],
    )

def convert_telecom(phone: str, use: str) -> Telecom:
    return Telecom(
        system="phone",
        value=phone,
        use=use,
    )

def convert_identifier(hl7_patient_id: str) -> Identifier:
    parts = hl7_patient_id.split("^")
    return Identifier(
        use="usual",
        type=CodeableConcept(
            coding=[
                Coding(
                    system="http://terminology.hl7.org/CodeSystem/v2-0203",
                    code=parts[4],
                )
            ]
        ),
        value=parts[0],
        assigner=Reference(
            display=parts[3],
        ),
    )

def convert_language(hl7_language: str) -> Communication:
    language_map = {
        "ENG": "en",
        "SPA": "es",
        "FRE": "fr",
        "GER": "de",
        "CHI": "zh",
        "JPN": "ja",
        "KOR": "ko",
        "ARA": "ar",
        "RUS": "ru",
        "POR": "pt",
        "ITA": "it",
        "VIE": "vi",
    }
    return Communication(
        language=CodeableConcept(
            coding=[
                Coding(
                    system="urn:ietf:bcp:47",
                    code=language_map.get(hl7_language, hl7_language.lower()),
                )
            ]
        ),
    )

def convert_marital_status(hl7_status: str) -> CodeableConcept:
    # HL7 and FHIR both use single letter codes but FHIR adds display names
    status_map = {
        "A": "Annulled",
        "D": "Divorced",
        "M": "Married",
        "S": "Never Married",
        "W": "Widowed",
        "L": "Legally Separated",
        "P": "Domestic Partner",
        "U": "Unknown",
    }
    return CodeableConcept(
        coding=[
            Coding(
                system="http://terminology.hl7.org/CodeSystem/v3-MaritalStatus",
                code=hl7_status,
                display=status_map.get(hl7_status, "Unknown"),
            )
        ]
    )


def pid_to_fhir_patient(pid_segment: PIDSegment) -> Patient:
    return Patient(
        name=[convert_name(pid_segment.patient_name)],
        gender=convert_gender(pid_segment.gender),
        birthDate=convert_dob(pid_segment.date_of_birth),
        identifier=[convert_identifier(pid_segment.patient_id)],
        address=[convert_address(pid_segment.address)],
        telecom=[convert_telecom(pid_segment.home_phone, 'home'), convert_telecom(pid_segment.business_phone, 'work')],
        communication=[convert_language(pid_segment.language)],
        maritalStatus=convert_marital_status(pid_segment.marital_status),
    )
