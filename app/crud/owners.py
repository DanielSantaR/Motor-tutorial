from app.db.mongodb import AsyncIOMotorClient
from pydantic import EmailStr
from typing import List

from app.core.config import database_name, owners_collection_name
from app.schemas.owner import Owner, OwnerUpdate


async def get_all(conn: AsyncIOMotorClient) -> List[Owner]:
    db_owners = conn[database_name][owners_collection_name].find()
    owners: List[Owner] = []
    async for owner in db_owners:
        owners.append(Owner(**owner))
    return owners

async def get_by_username(conn: AsyncIOMotorClient, username: str) -> Owner:
    owner = await conn[database_name][owners_collection_name].find_one({"username": username})
    if owner:
        return Owner(**owner)


async def get_by_email(conn: AsyncIOMotorClient, email: EmailStr) -> Owner:
    owner = await conn[database_name][owners_collection_name].find_one({"email": email})
    if owner:
        return Owner(**owner)


async def insert(conn: AsyncIOMotorClient, owner: Owner) -> Owner:
    await conn[database_name][owners_collection_name].insert_one(owner.dict())
    return owner


async def update(conn: AsyncIOMotorClient, username: str, owner: OwnerUpdate) -> Owner:
    dbowner = await get_by_username(conn, username)
    dbowner.name = owner.name or dbowner.name
    dbowner.surname = owner.surname or dbowner.surname
    dbowner.username = owner.username or dbowner.username
    dbowner.email = owner.email or dbowner.email
    dbowner.password = owner.password or dbowner.password
    await conn[database_name][owners_collection_name]\
        .update_one({"username": dbowner.username}, {'$set': dbowner.dict()})
    return dbowner


async def delete(conn: AsyncIOMotorClient, username: str) -> Owner:
    dbowner = await get_by_username(conn, username)
    if not dbowner:
        return None

    await conn[database_name][owners_collection_name].delete_one({"username": username})
    return dbowner
