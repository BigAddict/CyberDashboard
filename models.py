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

class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    status: str = Field(default="active")  # active | completed
    amount_paid: int = Field(default=0)
    payment_status: str = Field(default="pending")  # pending | paid