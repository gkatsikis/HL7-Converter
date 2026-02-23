# HL7 Converter

A FastAPI microservice that parses HL7 v2 messages and converts them to FHIR R4 resources.

## What it does

1. Accepts a raw HL7 v2 message (via API or the built-in web UI)
2. Parses it into a dict of segments keyed by segment type (e.g. `MSH`, `PID`, `PV1`)
3. Maps the relevant segments to FHIR-compliant Pydantic models
4. Returns a FHIR resource as JSON

Currently supports converting the **PID segment** to a **FHIR Patient** resource.

## Stack

- **FastAPI** — API framework
- **Pydantic** — FHIR resource modeling and validation
- **Uvicorn** — ASGI server
- **HTMX** — built-in web UI
- **pytest** — testing

## Project structure

```
app/
  main.py              # FastAPI app entry point
  parser/
    hl7_parser.py      # Parses raw HL7 v2 message into a dict of segments
  models/
    hl7_segments.py    # HL7 segment models (e.g. PIDSegment)
    fhir_resources.py  # FHIR resource models (e.g. Patient)
  transformer/
    to_fhir.py         # Converts HL7 segment models to FHIR resources
  routers/
    convert.py         # POST /convert endpoint
  templates/
    index.html         # Web UI
tests/
  test_hl7_parser.py
  test_hl7_segments.py
  test_to_fhir.py
```

## Running locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
uvicorn app.main:app --reload
```

The web UI is available at `http://localhost:8000`.

## API

### `POST /convert`

Accepts a raw HL7 v2 message and returns a FHIR Patient resource.

**Request** (JSON body or form field `hl7_message`):
```
MSH|^~\&|HospitalApp|MainHospital|...
PID|1||MRN12345^^^MainHospital^MR||Doe^John^A||19800115|M|...
```

**Response**:
```json
{
  "resourceType": "Patient",
  "identifier": [...],
  "name": [...],
  "gender": "male",
  "birthDate": "1980-01-15",
  ...
}
```

Also supports HTMX requests — returns an HTML fragment instead of JSON when the `HX-Request` header is present.

### `GET /health`

```json
{ "status": "ok" }
```

## Running tests

```bash
pytest tests/
```
