from .routers import metadata
from .db import database
from .dependencies import get_db
from fastapi import FastAPI, Depends

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Metadata-API",
    description="Metadata internal API to interact with metadata files",
    dependencies=[Depends(get_db)],
    docs_url="/",
    redoc_url=None
)

app.include_router(metadata.router)

