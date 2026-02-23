from app.parser.hl7_parser import hl7_parser

hl7_sample = """MSH|^~\&|HospitalApp|MainHospital|InsuranceApp|InsuranceCo|20231215120000||ADT^A01|MSG00001|P|2.5
EVN|A01|20231215120000
PID|1||MRN12345^^^MainHospital^MR||Doe^John^A||19800115|M|||123 Main St^^Springfield^IL^62701||555-867-5309|555-555-1234|ENG|M|CHR|ACCT001
PV1|1|I|ICU^101^A|||^Smith^Robert^J^^^MD|^Jones^Sarah^M^^^MD||MED||||7||^Smith^Robert^J^^^MD|IP||||||||||||||||||||||||||20231215120000"""

fhir_standard = {
    "resourceType": "Patient",
    "identifier": [
        {
            "use": "usual",
            "type": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                        "code": "MR",
                    }
                ]
            },
            "value": "MRN12345",
            "assigner": {"display": "MainHospital"},
        }
    ],
    "name": [{"use": "official", "family": "Doe", "given": ["John", "A"]}],
    "gender": "male",
    "birthDate": "1980-01-15",
    "address": [
        {
            "use": "home",
            "line": ["123 Main St"],
            "city": "Springfield",
            "state": "IL",
            "postalCode": "62701",
        }
    ],
    "telecom": [
        {"system": "phone", "value": "555-867-5309", "use": "home"},
        {"system": "phone", "value": "555-555-1234", "use": "work"},
    ],
    "communication": [
        {"language": {"coding": [{"system": "urn:ietf:bcp:47", "code": "en"}]}}
    ],
    "maritalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus",
                "code": "M",
                "display": "Married",
            }
        ]
    },
}

parsed_output = {
    "MSH": [
        "MSH",
        "^~\\&",
        "HospitalApp",
        "MainHospital",
        "InsuranceApp",
        "InsuranceCo",
        "20231215120000",
        "",
        "ADT^A01",
        "MSG00001",
        "P",
        "2.5",
    ],
    "EVN": ["EVN", "A01", "20231215120000"],
    "PID": [
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
    ],
    "PV1": [
        "PV1",
        "1",
        "I",
        "ICU^101^A",
        "",
        "",
        "^Smith^Robert^J^^^MD",
        "^Jones^Sarah^M^^^MD",
        "",
        "MED",
        "",
        "",
        "",
        "7",
        "",
        "^Smith^Robert^J^^^MD",
        "IP",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "20231215120000",
    ],
}


def test_hl7_parser():
    """test that the hl7 parses the raw v2 message into a dict of lists of values per segment"""

    payload = hl7_parser(hl7_sample)

    assert set(payload.keys()) == {"MSH", "EVN", "PID", "PV1"}

    assert payload["PID"][5] == "Doe^John^A"
    assert payload["PID"][7] == "19800115"
    assert parsed_output == payload
