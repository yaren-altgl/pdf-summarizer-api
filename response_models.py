from pydantic import BaseModel

class SummaryResponse(BaseModel):
    summary: str
    detected_language: str
    used_language: str
