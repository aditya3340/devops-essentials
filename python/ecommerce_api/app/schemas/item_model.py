from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class Item(BaseModel):
    name: str
    price: float
    store_id: UUID
    description: Optional[str] = None
    
class ItemOut(BaseModel):
    item_id: UUID
    name: str
    price: float
    store_id: UUID
    description: str | None = None
    
    
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
    
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    store_id: Optional[UUID] = None
    description: str | None = None

class ItemCreateResponse(BaseModel):
    message: str
    item: ItemOut

class ItemDeleteResponse(BaseModel):
    message: str
    item: ItemOut