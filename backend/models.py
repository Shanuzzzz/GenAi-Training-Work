from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Demographics for recommendations
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True) # Male, Female, Other
    state = Column(String, nullable=True)
    caste_category = Column(String, nullable=True) # General, OBC, SC, ST
    occupation = Column(String, nullable=True)
    annual_income = Column(Integer, nullable=True)
    
    saved_schemes = relationship("SavedScheme", back_populates="user")
    chat_history = relationship("ChatHistory", back_populates="user")


class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    department = Column(String, index=True)
    state = Column(String, index=True) # "Central" or specific state
    eligibility_criteria = Column(JSON) # Store structured criteria
    benefits = Column(Text)
    application_process = Column(Text)
    documents_required = Column(JSON)
    url = Column(String, nullable=True)


class SavedScheme(Base):
    __tablename__ = "saved_schemes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scheme_id = Column(Integer, ForeignKey("schemes.id"))
    saved_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="saved_schemes")
    scheme = relationship("Scheme")


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_id = Column(String, index=True)
    role = Column(String) # "user" or "assistant"
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="chat_history")
