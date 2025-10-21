from api.utils.string_utilities import word_count, sentence_length, is_palindrome, sha256_hasher, unique_characters, character_frequency_mapper
from api.v1.models.string_information import StringInformation
from api.v1.schemas.string_information import AnalyzeString
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from api.db.database import get_db
from typing import Optional
import re


strings_router = APIRouter(tags=["Strings"])

# post endpoint to analyze a string and return important information on it
@strings_router.post("/strings", status_code=status.HTTP_201_CREATED)
def string_analysis(strings: AnalyzeString, db: Session = Depends(get_db)):

    # carry out a check to see if the string already
    existing_string = db.query(StringInformation).filter(StringInformation.value == strings.value).first()
    if existing_string:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail= "String already exists in the system"
        )

    # check if the data type for the field is correct
    if not isinstance(strings.value, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid data type for 'value' (must be string)",
        )

    # check if the input field is empty
    if not strings.value:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail= "Invalid request body or missing 'value' field"
        )

    # analyze the string
    length = sentence_length(strings.value)
    palindrome_status = is_palindrome(strings.value)
    unique_characters_value = unique_characters(strings.value)
    word_count_value = word_count(strings.value)
    sha256_hash = sha256_hasher(strings.value)
    character_frequency_map = character_frequency_mapper(strings.value)

    # store the analyzed data in the database

    new_string = StringInformation(
        id=sha256_hash,
        value=strings.value,
        length=length,
        is_palindrome=palindrome_status,
        unique_characters_count=unique_characters_value[0],
        unique_characters_list=",".join(unique_characters_value[1]),
        word_count=word_count_value,
    )

    db.add(new_string)
    db.commit()
    db.refresh(new_string)

    # return the analyzed data

    return {
        "id": new_string.id,
        "value": new_string.value,
        "properties":{
            "length": new_string.length,
            "is_palindrome": new_string.is_palindrome,
            "unique_characters": new_string.unique_characters_count,
            "word_count": new_string.word_count,
            "sha256_hash": sha256_hash,
            "character_frequency_map": character_frequency_map
        },
        "created_at": new_string.created_at
    }


# get endpoint to retrieve info on a specific string
@strings_router.get("/strings/{string_value}", status_code=status.HTTP_200_OK)
def get_string_information(string_value: str, db: Session = Depends(get_db)):

    # check if the string exists in the database
    string_info = db.query(StringInformation).filter(StringInformation.value == string_value).first()
    if not string_info:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail= "String does not exist in the system"
        )

    character_frequency_map = character_frequency_mapper(string_value)

    # return the strings information

    return {
        "id": string_info.id,
        "value": string_info.value,
        "properties": {
            "length": string_info.length,
            "is_palindrome": string_info.is_palindrome,
            "unique_characters": string_info.unique_characters_count,
            "word_count": string_info.word_count,
            "sha256_hash": string_info.id,
            "character_frequency_map": character_frequency_map,
        },
        "created_at": string_info.created_at
    }

# get endpoint to retrieve all strings with filtering
def get_all_strings(
    is_palindrome: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    word_count: Optional[int] = None,
    contains_character: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Validate query parameters
    if contains_character is not None and (not isinstance(contains_character, str) or len(contains_character) != 1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="contains_character must be a single character string"
        )
    if min_length is not None and (not isinstance(min_length, int) or min_length < 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_length must be a non-negative integer"
        )
    if max_length is not None and (not isinstance(max_length, int) or max_length < 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="max_length must be a non-negative integer"
        )
    if word_count is not None and (not isinstance(word_count, int) or word_count < 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="word_count must be a non-negative integer"
        )
    if is_palindrome is not None and not isinstance(is_palindrome, bool):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="is_palindrome must be a boolean"
        )

    query = db.query(StringInformation)
    if is_palindrome is not None:
        query = query.filter(StringInformation.is_palindrome == is_palindrome)
    if min_length is not None:
        query = query.filter(StringInformation.length >= min_length)
    if max_length is not None:
        query = query.filter(StringInformation.length <= max_length)
    if word_count is not None:
        query = query.filter(StringInformation.word_count == word_count)
    if contains_character is not None:
        query = query.filter(StringInformation.value.contains(contains_character))

    results = query.all()
    data = []
    for string_obj in results:
        data.append({
            "id": string_obj.id,
            "value": string_obj.value,
            "properties": {
                "length": string_obj.length,
                "is_palindrome": string_obj.is_palindrome,
                "unique_characters": string_obj.unique_characters_count,
                "word_count": string_obj.word_count,
                "sha256_hash": string_obj.id,
                "character_frequency_map": character_frequency_mapper(string_obj.value)
            },
            "created_at": string_obj.created_at
        })
    filters_applied = {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_character": contains_character
    }
    return {
        "data": data,
        "count": len(data),
        "filters_applied": filters_applied
    }

@strings_router.get("/strings/filter-by-natural-language", status_code=status.HTTP_200_OK)
def filter_by_natural_language(query: str, db: Session = Depends(get_db)):
    original_query = query
    parsed_filters = {}
    query_lower = query.lower()
    # Basic parsing for example queries
    if "single word" in query_lower:
        parsed_filters["word_count"] = 1
    if "palindromic" in query_lower:
        parsed_filters["is_palindrome"] = True
    match = re.search(r"longer than (\d+) characters", query_lower)
    if match:
        parsed_filters["min_length"] = int(match.group(1)) + 1
    match = re.search(r"containing the letter ([a-z])", query_lower)
    if match:
        parsed_filters["contains_character"] = match.group(1)
    match = re.search(r"contain the first vowel", query_lower)
    if match:
        parsed_filters["contains_character"] = "a"  # heuristic: 'a' as first vowel
    # If no filters parsed, return error
    if not parsed_filters:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse natural language query"
        )
    # Check for conflicting filters (example: negative values)
    if (
        "min_length" in parsed_filters and parsed_filters["min_length"] < 0
    ) or (
        "word_count" in parsed_filters and parsed_filters["word_count"] < 0
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Query parsed but resulted in conflicting filters"
        )
    # Build query
    query_obj = db.query(StringInformation)
    if "is_palindrome" in parsed_filters:
        query_obj = query_obj.filter(StringInformation.is_palindrome == parsed_filters["is_palindrome"])
    if "min_length" in parsed_filters:
        query_obj = query_obj.filter(StringInformation.length >= parsed_filters["min_length"])
    if "word_count" in parsed_filters:
        query_obj = query_obj.filter(StringInformation.word_count == parsed_filters["word_count"])
    if "contains_character" in parsed_filters:
        query_obj = query_obj.filter(StringInformation.value.contains(parsed_filters["contains_character"]))
    results = query_obj.all()
    data = []
    for string_obj in results:
        data.append({
            "id": string_obj.id,
            "value": string_obj.value,
            "properties": {
                "length": string_obj.length,
                "is_palindrome": string_obj.is_palindrome,
                "unique_characters": string_obj.unique_characters_count,
                "word_count": string_obj.word_count,
                "sha256_hash": string_obj.id,
                "character_frequency_map": character_frequency_mapper(string_obj.value)
            },
            "created_at": string_obj.created_at
        })
    return {
        "data": data,
        "count": len(data),
        "interpreted_query": {
            "original": original_query,
            "parsed_filters": parsed_filters
        }
    }

@strings_router.delete("/strings/{string_value}", status_code=status.HTTP_200_OK)
def delete_string(string_value: str, db: Session = Depends(get_db)):
    string_obj = db.query(StringInformation).filter(StringInformation.value == string_value).first()
    if not string_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system"
        )
    db.delete(string_obj)
    db.commit()
    return {"message": f"String '{string_value}' and its information have been deleted."}

