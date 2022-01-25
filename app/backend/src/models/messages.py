from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, Boolean, Text, DateTime, func, String 

from database import Base, database


class MessageManager:
    def __init__(self, model_cls):
        self.table: sqlalchemy.Table = model_cls.__table__


    async def create(self, *args, **kwargs):
        """
        Create Message

        Создание сообщения в локальной базе данных
        """
        date_created = datetime.utcnow()
        returning = await database.fetch_one(self.table.insert().values(date_created=date_created, **kwargs).returning(self.table.c.id))
        kwargs['id'] = returning[0]
        kwargs['date_created'] = date_created
    
        return Message(**kwargs)

    async def get_message(self, message_id):
        """
        Получение одного сообщения по message_id
        :param message_id: ID сообщения
        :return: Message
        """

        data = await database.fetch_one(self.table.select(Message.id == message_id))

        if data is not None:
            return Message(**data)
        return None


    

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    body = Column(Text)
    date_created = Column(DateTime, server_default=func.now())
    client_id = Column(Integer, nullable=True)
    with_bot = Column(Boolean, nullable=True)
    bot_script = Column(String, nullable=True)

    objects: MessageManager = None


Message.objects = MessageManager(model_cls=Message)
