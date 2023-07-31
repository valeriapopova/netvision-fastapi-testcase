import uuid

from pydantic.main import BaseModel


class CreateEntry(BaseModel):
    text: str

    class Config:
        schema_extra = {
            'example': {
                'text': 'example text'
            }
        }


class Entry(BaseModel):
    text: str
    uuid: uuid.UUID

    class Config:
        schema_extra = {
            'example': {
                'text': 'example text',
                'uuid': 'eddd8cd7-1128-4b83-98d4-7cde1514625e'
            }
        }


class BaseResp(BaseModel):
    status: str

    class Config:
        schema_extra = {
            'example': {
                'status': 'accepted',
            },
        }


class HealthResp(BaseResp):
    message: str

    class Config:
        schema_extra = {
            'example': {
                'status': 'ok',
                'message': 'ready and able',
            },
        }
