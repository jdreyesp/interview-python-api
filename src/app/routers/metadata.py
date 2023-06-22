from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..db import crud
from ..dependencies import get_db
from ..model.metadata import Metadata, MetadataCreate, MetadataDelete

router = APIRouter(
    prefix="/metadata",
    tags=["metadata"],
    responses={404: {"description": "Not found"}, 500: {"description": "Internal Server Error"}},
)

@router.get("", summary="List of metadata records", response_model=list[Metadata])
def get_metadata_items(db: Session = Depends(get_db)):
    metadata_list: [Metadata] = crud.get_metadata_list(db)
    if not metadata_list:
        raise HTTPException(status_code=404, detail="No metadata")

    return metadata_list

@router.get("/{id}", summary="Get metadata record by ID", response_model=Metadata)
def get_metadata_item(id: str, db: Session = Depends(get_db)):
    metadata: Metadata = crud.get_metadata(db, id)
    if not metadata:
        raise HTTPException(status_code=404, detail="No metadata")

    return metadata

@router.post("", summary="Creates a new metadata record", response_model=Metadata)
def create_metadata(metadata: MetadataCreate, db: Session = Depends(get_db)):
    return crud.create_metadata(db, metadata)

@router.delete("/{id}", summary="Deletes a metadata record", response_model=MetadataDelete)
def delete_metadata(id: str, db: Session = Depends(get_db)):
    metadata_deleted: MetadataDelete = crud.delete_metadata(db, id)
    if metadata_deleted.deleted == 0:
        raise HTTPException(status_code=404, detail="Metadata not found")
    return metadata_deleted