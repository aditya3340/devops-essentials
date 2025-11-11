from fastapi import FastAPI
from app.routes import item_routes, store_routes
from app.database import engine
from sqlalchemy import inspect
from contextlib import asynccontextmanager
from app.database import wait_for_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting FastAPI...")

    wait_for_db(3,3)
    
    
    inspector = inspect(engine)
    print(f"tables: {inspector.get_table_names()}")
    
    
    
    print("Connected to database.")
    yield
    print("Shutting down FastAPI...")


app = FastAPI(lifespan=lifespan)


app.include_router(store_routes.router)
app.include_router(item_routes.router)

@app.get("/")
def root():
    return {"Message": "FastAPI Store Service!"}