from pydantic import BaseModel, Field


class AnalyzeString(BaseModel):
    value: str = Field(..., description="The string to be analyzed")