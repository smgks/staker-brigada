from fastapi import FastAPI
from app.api import auth_router, trader_router, items_router, trader_management_router


app = FastAPI()

# app.include_router(auth_router, prefix="/")
app.include_router(auth_router, tags=["auth"], prefix="/auth")
app.include_router(trader_router, tags=["trader"], prefix="/trader")
app.include_router(items_router, tags=["items"], prefix="/items")
app.include_router(trader_management_router, tags=["trader management"], prefix="/trader_mgmnt")
