from sqlalchemy import Column, Integer, String, Text, DateTime
from backend.db.database import Base
from datetime import datetime


class SelectedText(Base):
    __tablename__ = "selected_texts"
    
    id = Column(Integer, primary_key = True, index = True)
    content = Column(Text, nullable= False)
    
    status = Column(
        String,
        default = "pending",
        nullable = False
    )
    
    retry_count = Column(
        Integer,
        default = 0,
        nullable = False
    )
    
    last_error = Column(
        Text,
        nullable = True,
    )
    
    created_at = Column(
        DateTime,
        default = datetime.utcnow,
        nullable = False
    )
    
    updated_at = Column(
        DateTime,
        default = datetime.utcnow,
        onupdate = datetime.utcnow,
        nullable = False
    )