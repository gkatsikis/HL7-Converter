from app.models.hl7_segments import parse_msh, parse_pid


def test_parse_msh():
    msh_list = [
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
    ]

    result = parse_msh(msh_list)

    assert result.field_separator == "|"
    assert result.encoding_chars == "^~\\&"
    assert result.sending_application == "HospitalApp"
    assert result.message_type == "ADT^A01"
    assert result.version_id == "2.5"
    assert result.security is None


def test_parse_pid():
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

    result = parse_pid(pid_list)

    assert result.patient_name == "Doe^John^A"
    assert result.home_phone == "555-867-5309"
    assert result.address == "123 Main St^^Springfield^IL^62701"
    assert result.patient_alias is None