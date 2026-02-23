from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.routers.convert import router

app = FastAPI(
    title="HL7 to FHIR Converter microservice",
    description="A microservice that converts HL7 messages to FHIR resources.",
    version="0.1.0",
)


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

app.include_router(router)

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    html_path = Path("app/templates/index.html")
    return html_path.read_text()