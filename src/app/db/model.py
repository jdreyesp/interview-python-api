from sqlalchemy import Text, Column, Integer, String, DateTime
from sqlalchemy.sql import func

from .database import Base


class Metadata(Base):
    __tablename__ = "metadata"

    id = Column(String, primary_key=True, index=True)
    registered_on = Column(DateTime(timezone=True), server_default=func.now())
    name = Column(String)
    payload = Column(Text)

