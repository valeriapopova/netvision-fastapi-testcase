import json

from uuid import UUID
from typing import List
from fastapi import Depends, HTTPException, Response
from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session

from config import PG_CONF
from server import crud, database, schemas

router = APIRouter()


def get_db():
    db = database.PGDB(**PG_CONF).session()
    try:
        yield db
    finally:
        db.close()


@router.get(
    path='/health',
    status_code=200,
    response_model=schemas.HealthResp,
)
async def health():
    """Method for checking application health"""

    return {
        'status': 'ok',
        'message': 'ready and able',
    }


@router.post("/new", response_model=List[schemas.CreateEntry])
async def create_new_entry(entries: List[schemas.CreateEntry],
                           db: Session = Depends(get_db)):
    """Create new entries"""
    return await crud.create_entry(entries=entries, db=db)


@router.get("/all")
async def get_all_entries(db: Session = Depends(get_db)):
    """Get all entries"""
    return await crud.get_all_entries(db=db)


@router.get("/{uuid:uuid}")
async def get_an_entry_by_uuid(uuid: UUID, db: Session = Depends(get_db)):
    """Get an entry by UUID"""
    entry = await crud.get_an_entry(uuid=uuid, db=db)
    if entry:
        return entry
    else:
        raise HTTPException(status_code=404, detail='No data')


@router.get("/{count:int}")
async def get_an_entry(count: int, db: Session = Depends(get_db)):
    """Get entries by count"""
    entry = await crud.get_entries_by_count(count=count, db=db)
    if entry:
        return entry
    else:
        raise HTTPException(status_code=404, detail='No data')


@router.delete("/{uuid:uuid}")
async def delete_an_entry(uuid: UUID, db: Session = Depends(get_db)):
    """Delete an entry by UUID"""
    entry = await crud.delete_an_entry(uuid=uuid, db=db)
    if entry:
        entry = {'response': 'Entry deleted successfully'}
        return Response(content=json.dumps(entry), status_code=200)
    else:
        raise HTTPException(status_code=404, detail='UUID is not found')
