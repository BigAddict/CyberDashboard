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
