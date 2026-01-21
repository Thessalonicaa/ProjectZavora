from pydantic import BaseModel
from datetime import datetime

class AttendanceCreate(BaseModel):
    name: str
    type: str

class AttendanceOut(BaseModel):
    id: int
    name: str
    type: str
    timestamp: datetime

    class Config:
        from_attributes = True
        

