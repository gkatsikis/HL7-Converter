from app.models.hl7_segments import parse_pid
from app.transformer.to_fhir import pid_to_fhir_patient


pid_list = [
    "PID",
    "1",
    "",
    "MRN12345^^^MainHospital^MR",
    "",
    "Doe^John^A",
    "",
    "19800115",
    "M",
    "",
    "",
    "123 Main St^^Springfield^IL^62701",
    "",
    "555-867-5309",
    "555-555-1234",
    "ENG",
    "M",
    "CHR",
    "ACCT001",
]


def test_pid_to_fhir_patient():
    pid_segment = parse_pid(pid_list)
    result = pid_to_fhir_patient(pid_segment)

    assert result.resourceType == "Patient"

    assert result.name[0].family == "Doe"
    assert result.name[0].given == ["John", "A"]
    assert result.name[0].use == "official"

    assert result.gender == "male"

    assert result.birthDate == "1980-01-15"

    assert result.identifier[0].value == "MRN12345"
    assert result.identifier[0].assigner.display == "MainHospital"
    assert result.identifier[0].type.coding[0].code == "MR"

    assert result.address[0].line == ["123 Main St"]
    assert result.address[0].city == "Springfield"
    assert result.address[0].state == "IL"
    assert result.address[0].postalCode == "62701"

    assert result.telecom[0].value == "555-867-5309"
    assert result.telecom[0].use == "home"
    assert result.telecom[1].value == "555-555-1234"
    assert result.telecom[1].use == "work"

    assert result.communication[0].language.coding[0].code == "en"

    assert result.maritalStatus.coding[0].code == "M"
    assert result.maritalStatus.coding[0].display == "Married"