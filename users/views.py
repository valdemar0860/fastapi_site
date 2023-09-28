from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import BaseUser
from . import crud
from core.models.db_helper import db_helper

router = APIRouter(prefix='/users')


@router.get('/get_user/')
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    return await crud.get_user(user_id=user_id, session=session)


@router.post('/create_user/')
async def create_user(
        user: BaseUser,
        session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    return await crud.create_user(user_in=user, session=session)


@router.delete('/delete_user/')
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    return await crud.delete_user(user_id=user_id, session=session)


@router.put('/permanent_update_user/')
async def permanent_update_user(
        user: BaseUser,
        user_id: int,
        session: AsyncSession = Depends(db_helper.get_scoped_session),
        partial: bool = False
):
    return await crud.update_user(user=user, user_id=user_id, session=session)


@router.patch('/update_user/')
async def update_user(
        user: BaseUser,
        user_id: int,
        session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    return await crud.update_user(user=user, user_id=user_id, session=session, partial=True)
