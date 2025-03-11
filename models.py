from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class CPU(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True, unique=True)
    ip_address: str = Field(index=True, unique=True)
    status: str = Field(default="offline")
    usage_percent: float = Field(default=0.0)
    temperature: float = Field(default=0.0)
    last_maintenance: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
