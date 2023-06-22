from typing import Optional

from pydantic import BaseModel
import datetime


class MetadataBase(BaseModel):
    registered_on: datetime.datetime = datetime.datetime.now()
    name: str
    payload: str

class MetadataCreate(MetadataBase):
    pass

class MetadataDelete(BaseModel):
    deleted: int

class Metadata(MetadataBase):
    id: str

    class Config:
        orm_mode = True
