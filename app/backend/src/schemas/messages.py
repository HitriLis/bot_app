from datetime import datetime
from pydantic import BaseModel


class Message(BaseModel):
    id: int = None
    body: str = None
    date_created: datetime = None
    client_id: int = None
    bot_script: str = None
 

    class Config:
        orm_mode = True
