from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class Store(BaseModel):
    name: str
    description: Optional[str] = None
    
class StoreOut(BaseModel):
    store_id: UUID
    name: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        
class StoreUpdate(BaseModel):
    store_id: UUID  
    name: Optional[str] = None
    description: Optional[str] = None
    
class StoreCreateResponse(BaseModel):
    message: str
    store: StoreOut
    
class StoreDeleteResponse(BaseModel):
    message: str
    store: StoreOut
          