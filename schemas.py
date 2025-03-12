from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CPUBase(BaseModel):
    name: str
    ip_address: str
    status: Optional[str] = "offline"
    usage_percent: Optional[float] = 0.0
    temperature: Optional[float] = 0.0
    last_maintenance: Optional[datetime] = None

class CPUCreate(CPUBase):
    pass

class CPUUpdate(CPUBase):
    pass

class CPUResponse(CPUBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True

class SessionBase(BaseModel):
    status: Optional[str] = "active"

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    status: Optional[str] = None
    amount_paid: Optional[int] = None
    payment_status: Optional[str] = None

class SessionResponse(SessionBase):
    id: int
    start_time: datetime
    end_time: Optional[datetime]
    duration_minutes: Optional[int]
    amount_paid: Optional[int] = None
    payment_status: Optional[str] = None

    class Config:
        orm_mode = True