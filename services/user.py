import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, insert, select, delete, update
from typing import Dict
from db.crud import new_crud
from db.models.user import User, user_master_association
from schemas.user import UserCreate


logger = logging.getLogger(__name__)


class UserService:

    def __init__(self, session:AsyncSession):
        self.session = session

    async def get_user(self, filters:Dict):
        query = select(User).filter_by(**filters)
        user = await new_crud.read(query, self.session)
        return user.scalar()
    
    async def add_master_to_user(self, user_id:int, master_chat_id:int):
        master = await self.get_user({"chat_id":master_chat_id})
        stmt = insert(user_master_association).values(user_id=user_id, master_id=master.id)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Master add to user successfully")

    async def create_user(self, user_data: UserCreate):
        user_dump = user_data.model_dump(exclude={"master_chat_id"})
        new_user = await new_crud.create(User(**user_dump), self.session)
        logger.info(f"User {new_user.name} created successfully")
        if user_data.master_chat_id is not None:
            await self.add_master_to_user(new_user.id, user_data.master_chat_id)
        return new_user
    
    async def delete_user(self, user_id:int):
        await new_crud.delete(delete(User).filter_by(id=user_id), self.session)

    async def deactivate_user(self, user_id:int):
        await new_crud.update(update(User).filter_by(id=user_id), self.session)

            
        
            
