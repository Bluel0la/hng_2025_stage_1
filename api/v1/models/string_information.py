from sqlalchemy import Column, String, Boolean, Integer, DateTime, Text
from api.db.database import Base
from datetime import datetime


class StringInformation(Base):
    __tablename__ = "StringInformation"
    
    id = Column(String, unique=True, index=True, primary_key=True)
    value = Column(String, nullable=False)
    length = Column(Integer, nullable=False)
    is_palindrome = Column(Boolean, nullable=False)
    unique_characters_count = Column(Integer, nullable=False)
    unique_characters_list = Column(Text, nullable=False)
    word_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)