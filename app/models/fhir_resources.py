from pydantic import BaseModel
from typing import Optional


class Coding(BaseModel):
    system: str
    code: str
    display: Optional[str] = None


class CodeableConcept(BaseModel):
    coding: list[Coding]


class Reference(BaseModel):
    display: str


class Identifier(BaseModel):
    use: str
    type: CodeableConcept
    value: str
    assigner: Reference


class HumanName(BaseModel):
    use: str
    family: str
    given: list[str]


class Address(BaseModel):
    use: str
    line: list[str]
    city: str
    state: str
    postalCode: str


class Telecom(BaseModel):
    system: str
    value: str
    use: str


class Communication(BaseModel):
    language: CodeableConcept


# Top level model
class Patient(BaseModel):
    resourceType: str = "Patient"
    identifier: list[Identifier]
    name: list[HumanName]
    gender: str
    birthDate: str
    address: list[Address]
    telecom: list[Telecom]
    communication: list[Communication]
    maritalStatus: CodeableConcept
