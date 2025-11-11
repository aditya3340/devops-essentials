from sqlalchemy import Column, String,Float, DateTime,ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Store(Base):
    __tablename__ = "store"
    
    store_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    items = relationship(
            "Item",
            back_populates="store", 
            cascade="all,delete, delete-orphan",
            passive_deletes=True
        )
    
    
class Item(Base):
    __tablename__ = "item"
    
    item_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String)
    store_id = Column(
            UUID(as_uuid=True),
            ForeignKey("store.store_id", ondelete="CASCADE"),
            nullable=False
        )
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    store = relationship("Store",back_populates="items", passive_deletes=True)
    