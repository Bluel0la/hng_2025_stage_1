from api.utils.string_utilities import word_count, sentence_length, is_palindrome, sha256_hasher, unique_characters, character_frequency_mapper
from api.v1.models.string_information import StringInformation
from api.v1.schemas.string_information import AnalyzeString
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.db.database import get_db




strings_router = APIRouter(tags=["Strings"])

# post endpoint to analyze a string and return important information on it
@strings_router.post("/strings", status_code=status.HTTP_201_CREATED)
def string_analysis(strings: AnalyzeString, db: Session = Depends(get_db)):
    
    #carry out a check to see if the string already