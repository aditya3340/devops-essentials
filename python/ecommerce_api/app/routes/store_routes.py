from fastapi import APIRouter, HTTPException,status,Depends
from app.schemas.store_model import Store,StoreOut, StoreUpdate, StoreCreateResponse, StoreDeleteResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app import db_models
from uuid import UUID
from typing import List


router = APIRouter(prefix="/store", tags=["Store"])

@router.get(
            "",
            status_code=status.HTTP_200_OK,
            response_model=List[StoreOut],
            summary="Get all stores."
            )
def get_stores(db: Session=Depends(get_db)):
    stores = db.query(db_models.Store).all()
    return stores 
    

# add store
@router.post(
            "", 
            status_code=status.HTTP_201_CREATED,
            response_model=StoreCreateResponse,
            summary="Create a store."
        )
def create_store(store: Store, db: Session=Depends(get_db)):
    
    store_data = store.model_dump()
    
    existing_store = db.query(db_models.Store).filter_by(name=store_data["name"]).first()
          
    # duplicate validation
    if existing_store:
        
        raise HTTPException(status_code=409, detail="Store already exists.")
    
    new_store = db_models.Store(**store_data)
    
    # add store in database
    try:
        db.add(new_store)
        db.commit()
        db.refresh(new_store)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error Occured while adding store in database. Error: {e}")
    
    return {"message": "Store created successfully.", "store": new_store}

# get single store 
@router.get(
            "/{id}", 
            response_model=StoreOut, 
            status_code=status.HTTP_200_OK, 
            summary="Get a store by ID"
        )
def get_store_details(id: UUID, db: Session=Depends(get_db)):
    
    store = db.query(db_models.Store).filter_by(store_id=id).first()
    
    if not store:
        raise HTTPException(404, detail="Store not found.")
    
    return store


@router.delete(
            "/{id}",
            status_code=status.HTTP_200_OK,
            response_model=StoreDeleteResponse,
            summary="Delete a store."
        )
def delete_store(id: UUID, db: Session=Depends(get_db)):
    
    store = db.query(db_models.Store).filter_by(store_id=id).first()
    
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    try:
        db.delete(store)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error occured while deleting a store. Error: {e}")
 
    return {"message": "Store deleted successfully", "store": store}



@router.put(
            "/{id}", 
            status_code=status.HTTP_200_OK, 
            response_model=StoreOut, 
            summary="Update a store."
        )
def update_store(id: UUID, updated_store: StoreUpdate, db: Session=Depends(get_db)):
    
    store = db.query(db_models.Store).filter_by(store_id=id).first()
    
    
    if not store:
        raise HTTPException(status_code=404, detail="Store not found.")
    
    for key, value in updated_store.model_dump(exclude_unset=True).items():
        setattr(store, key, value)
    
    try:
        db.commit()
        db.refresh(store)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error Occurred while updating the store attributes. Error: {e}")
    
    return store 