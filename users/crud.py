from typing import Type, Sequence

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select, Result, func
from datetime import datetime

from core.models.models import User
from .schemas import BaseUser, CreateUser


async def get_user(session: AsyncSession, user_id: int) -> Type[User] | None:
    try:
        user = await session.get(User, user_id)
        if user is None:
            raise NoResultFound("User not found")
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


async def get_users(session: AsyncSession) -> Sequence[User]:
    try:
        users = await session.execute(select(User))
        if users:
            return users.scalars().all()
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


async def create_user(session: AsyncSession, user_in: BaseUser) -> CreateUser:
    try:
        count_users = await session.scalar(select(func.count()).select_from(User))
        user = User(
            id=count_users,
            registered_at=datetime.utcnow(),
            **user_in.model_dump()
        )
        session.add(user)
        await session.commit()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
    return user


async def delete_user(session: AsyncSession, user_id: int) -> None:
    try:
        user = await session.get(User, user_id)
        if user:
            await session.delete(user)
            await session.commit()
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


async def update_user(
        session: AsyncSession,
        user_id: int,
        user: BaseUser,
        partial: bool = False,
) -> Type[User]:
    try:
        find_user = await session.get(User, user_id)
        if user:
            find_user.name = user.name
            find_user.email = user.email
            find_user.password = user.password

            await session.commit()
            return find_user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()
