from app.crud import owners
from app.schemas import owner
from app.db.mongodb import AsyncIOMotorClient, get_database
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List


router = APIRouter()


@router.get("/username/all", response_model=List[owner.Owner])
async def get_all(db: AsyncIOMotorClient = Depends(get_database)):
    db_owners = await owners.get_all(conn=db)
    if len(db_owners) == 0:
        raise HTTPException(
            status_code=404, detail=f"No owners found in the DB"
        )
    return db_owners


@router.get("/username/{username}", response_model=owner.Owner)
async def get_by_username(username: str, db: AsyncIOMotorClient = Depends(get_database)):
    db_owners = await owners.get_by_username(conn=db, username=username)
    if not db_owners:
        raise HTTPException(
            status_code=404, detail=f"No owners found with username {username}"
        )
    return db_owners


@router.get("/email/{email}", response_model=owner.Owner)
async def get_by_email(email: str, db: AsyncIOMotorClient = Depends(get_database)):
    db_owners = await owners.get_by_email(conn=db, email=email)
    if not db_owners:
        raise HTTPException(
            status_code=404, detail=f"No owners found with email {email}"
        )
    return db_owners


@router.post("/insert/", response_model=owner.Owner)
async def insert(owner: owner.Owner, db: AsyncIOMotorClient = Depends(get_database)):
    await field_validation(owner=owner, db=db)
    inserted_owner = await owners.insert(conn=db, owner=owner)
    return inserted_owner


@router.put("/update/{username}", response_model=owner.Owner)
async def update(owner: owner.OwnerUpdate, username: str, db: AsyncIOMotorClient = Depends(get_database)):
    await field_validation(owner=owner, db=db)
    db_owner = await owners.update(conn=db, owner=owner, username=username)
    if db_owner is None:
        raise HTTPException(
            status_code=404, detail=f"Owner with username {username} not found"
        )
    return db_owner


@router.delete("/username/{username}", response_model=owner.Owner)
async def delete(username: str, db: AsyncIOMotorClient = Depends(get_database)):
    db_owners = await owners.delete(conn=db, username=username)
    if not db_owners:
        raise HTTPException(
            status_code=404, detail=f"No owners found with username {username}"
        )
    return db_owners


async def field_validation(owner: owner.Owner, db: AsyncIOMotorClient = Depends(get_database)):
    db_owner_username = await owners.get_by_username(
        conn=db, username=owner.username)
    if db_owner_username is not None:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )

    db_owner_email = await owners.get_by_email(conn=db, email=owner.email)
    if db_owner_email is not None:
        raise HTTPException(
            status_code=404, detail="email already registered"
        )
    else:
        return None
