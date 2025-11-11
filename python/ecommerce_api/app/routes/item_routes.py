from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.item_model import Item,ItemOut, ItemUpdate, ItemCreateResponse, ItemDeleteResponse
from app.database import get_db
from sqlalchemy.orm import Session
from app import db_models
from uuid import UUID
from typing import List
 
router = APIRouter(prefix="/item", tags=["Item"])   
   

@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=List[ItemOut],
            summary="Get all items from item table"
            )
def get_all_item(db: Session=Depends(get_db)):
    items = db.query(db_models.Item).all()
    return items
    


@router.post("", 
             status_code=status.HTTP_201_CREATED,
             response_model=ItemCreateResponse,
             summary="Create a new item."
             )
def create_item(item: Item, db: Session=Depends(get_db)):

    item_data = item.model_dump()
    
    # Check if store exists from db
    store = db.query(db_models.Store).filter_by(store_id=item_data["store_id"]).first()
    
    
    # Check if store exists
    if not store:  
        raise HTTPException(
                status_code=404, 
                detail=f"Store Not Found with the store_id {item_data['store_id']}"
            )
        
    # items with similar names in same store
    existing_item = db.query(db_models.Item).filter_by(name=item_data["name"], store_id=item_data["store_id"]).first()
    
    # duplicate item validation
    if existing_item:
        
        raise HTTPException(status_code=400, detail=f"Item already exists")
 
    # add item to the database
    new_item = db_models.Item(**item_data)
    
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error occurred while Adding item. {e}")
    
    return {"message": "Item created Successfully.", "item": new_item}
    


@router.get("/{id}", 
            response_model=ItemOut,
            status_code=status.HTTP_200_OK,
            summary="Get an individual item from item table."
            )
def get_item(id: UUID, db: Session=Depends(get_db)):
    
    item = db.query(db_models.Item).filter_by(item_id=id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item


         
@router.delete("/{id}", 
               status_code=status.HTTP_200_OK, 
               response_model=ItemDeleteResponse,
               summary="Delete an item by ID"
            )
def delete_item(id: UUID, db: Session=Depends(get_db)):
    
    # check if item exists in database
    item = db.query(db_models.Item).filter_by(item_id=id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    
    # delete item from database
    try:
        db.delete(item)
        db.commit()
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error occurred while deleting item. {e}")
        
    return {"message": "Item deleted Successfully.", "item": item}


@router.put("/{id}",
            status_code=status.HTTP_200_OK, 
            summary="Update an existing item",
            response_model=ItemOut
        )
def update_item(id: UUID, updated_data: ItemUpdate, db: Session=Depends(get_db)):
    
    # check if item exists in database
    item = db.query(db_models.Item).filter_by(item_id=id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    
    try:
        db.commit()
        db.refresh(item)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error occurred while updating item. {e}")
    
    return {"message": "Item updated successfully.", "item": item}
        
  