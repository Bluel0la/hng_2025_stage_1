from pydantic import BaseModel, Field


class AnalyzeString(BaseModel):
    input_string: str = Field(..., description="The string to be analyzed")