from app.schemas import UserCredentials
from app.crud import create_user
from sqlalchemy.orm import Session
from app.db import SessionLocal
import asyncio


async def _create_user(
    db: Session,
):
    user = UserCredentials(
        login="admin",
        password="admin",
    )
    return create_user(db, user)


async def main():
    db = SessionLocal()
    user = await _create_user(db)
    print(user)
    db.close()

if __name__ == "__main__":
    asyncio.run(main())
