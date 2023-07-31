import uuid
from typing import List, Any

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

import models
import schemas


async def create_entry(db: Session, entries: List[schemas.CreateEntry]) -> list[models.Entry_DB]:
    db_entry = [models.Entry_DB(text=entry.text, uuid=uuid.uuid1()) for entry in entries]
    for entry in db_entry:
        db.add(entry)
        db.commit()
        db.refresh(entry)
    return db_entry


async def get_all_entries(db: Session) -> list[dict[str, str | Any]] | bool:
    entries = db.query(models.Entry_DB).all()
    if entries:
        entries_list = list()
        for entry in entries:
            entries_list.append({"uuid": str(entry.uuid), "text": entry.text})
        return entries_list
    else:
        return False


async def get_entries_by_count(db: Session, count: int) -> list[dict[str, str | Any]] | bool:
    entries = db.query(models.Entry_DB).limit(count).all()
    if entries:
        entries_list = list()
        for entry in entries:
            entries_list.append({"uuid": str(entry.uuid), "text": entry.text})
        return entries_list
    else:
        return False


async def get_an_entry(uuid: uuid.UUID, db: Session) -> dict[str, str | Any] | bool:
    try:
        entry = db.query(models.Entry_DB).filter(models.Entry_DB.uuid == uuid).one()
        entry = {"uuid": str(entry.uuid), "text": entry.text}
        return entry
    except NoResultFound:
        return False


async def delete_an_entry(uuid: uuid.UUID, db: Session) -> bool:
    try:
        entry = db.query(models.Entry_DB).filter(models.Entry_DB.uuid == uuid).one()
        db.delete(entry)
        db.commit()
        return True
    except NoResultFound:
        return False



