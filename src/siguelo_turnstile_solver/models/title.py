from pydantic.dataclasses import dataclass


@dataclass
class Title:
    registry_office: str
    year: str
    number: str
