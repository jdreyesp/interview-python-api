from sqlalchemy.orm import Session
import uuid

from . import model
from ..model import metadata

def create_metadata(db: Session, metadata: metadata.MetadataCreate):
    db_metadata = model.Metadata(id=str(uuid.uuid4()), name=metadata.name, payload=metadata.payload)
    db.add(db_metadata)
    db.commit()
    db.refresh(db_metadata)
    return db_metadata

def get_metadata_list(db: Session, skip: int = 0, limit: int = 100) -> [metadata.Metadata]:
    return db.query(model.Metadata).offset(skip).limit(limit).all()

def get_metadata(db: Session, id: str) -> metadata.Metadata:
    return db.query(model.Metadata).filter(model.Metadata.id == id).first()

def delete_metadata(db: Session, id: str) -> metadata.MetadataDelete:
    metadata_deleted: metadata.MetadataDelete = metadata.MetadataDelete(deleted=db.query(model.Metadata).filter(model.Metadata.id == id).delete())
    db.commit()
    return metadata_deleted