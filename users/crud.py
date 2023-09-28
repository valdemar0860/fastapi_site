from typing import Type

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from core.models.models import User
from .schemas import BaseUser, User
from core.models import models


async def get_user(session: AsyncSession, user_id: int) -> Type[User] | None:
    try:
        user = await session.get(models.User, user_id)
        if user is None:
            raise NoResultFound("User not found")
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")


async def create_user(session: AsyncSession, user_in: BaseUser) -> User:
    user = models.User(
        id=2,
        registered_at=datetime.utcnow(),
        **user_in.model_dump()
    )
    try:
        session.add(user)
        await session.commit()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
    return user


async def delete_user(session: AsyncSession, user_id: int) -> None:
    try:
        user = await session.get(models.User, user_id)

        await session.delete(user)
        await session.commit()
    except NoResultFound:
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
        find_user = await session.get(models.User, user_id)

        find_user.name = user.name
        find_user.email = user.email
        find_user.password = user.password

        await session.commit()
        return find_user
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()
