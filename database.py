from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()
engine = create_engine('sqlite:///data/talentflow.db', echo=False)
Session = sessionmaker(bind=engine)

class Screening(Base):
    __tablename__ = 'screenings'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    job_title = Column(String(200))
    job_description = Column(Text)
    candidate_name = Column(String(100))      # Original (stored securely)
    redacted_name = Column(String(100))
    score = Column(Float)
    match_percentage = Column(Float)
    skills = Column(JSON)
    experience = Column(Text)
    education = Column(Text)
    bias_redacted = Column(Text)
    fraud_flag = Column(String(50))
    explanation = Column(Text)
    raw_file_path = Column(String(500))

def init_db():
    os.makedirs('data', exist_ok=True)
    Base.metadata.create_all(engine)

def get_session():
    return Session()