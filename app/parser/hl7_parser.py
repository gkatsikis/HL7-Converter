def hl7_parser(hl7_message: str) -> dict:
    parsed_output = {}
    raw_segments = hl7_message.strip().splitlines()

    for segment in raw_segments:
        split_segment = segment.split("|")
        parsed_output[split_segment[0]] = split_segment

    print("parsed output ", parsed_output)

    return parsed_output
