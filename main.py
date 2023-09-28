import uvicorn
from fastapi import FastAPI
# from multiprocessing import freeze_support
from contextlib import asynccontextmanager
from users.views import router as users_router
from core.models.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(db_helper.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)

if __name__ == '__main__':
    # freeze_support()
    uvicorn.run('main:app', reload=True)
