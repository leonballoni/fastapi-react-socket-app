from typing import List, Union, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import pytz


desired_timezone = 'America/Sao_Paulo'
timezone_obj = pytz.timezone(desired_timezone)


class Messages(BaseModel):
    message_id: Optional[int] = 1
    username: str
    message: str
    date: Optional[Union[datetime, str]] = Field(default=None)
    
    @classmethod
    def generate_default_date(cls):
        return datetime.now(timezone_obj).strftime("%Y/%m/%d %H:%M:%S")

    def __init__(self, **data):
        if data.get('date') is None:
            data['date'] = self.generate_default_date()
        super().__init__(**data)


class Chats(BaseModel):
    chat_id: Optional[int] = None
    chat: str
    owner: str
    messages: List[Messages]


class UserAuth(BaseModel):
    username: str
    password: str
