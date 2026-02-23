from fastapi import FastAPI
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
