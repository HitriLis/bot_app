import pytest
from database import database
from models import Message


@pytest.mark.asyncio
async def test_message_create():
    await database.connect()
    tx = await database.transaction()
    client_id = 22
    message = await Message.objects.create(client_id=client_id, body='Test',  bot_script='script_name')

    try:
        assert message.client_id == client_id
    finally:
        await tx.rollback()
  
    await database.disconnect()


@pytest.mark.asyncio
async def test_get_last_script_bot():
    await database.connect()
    tx = await database.transaction()
    client_id = 22
    message = await Message.objects.create(client_id=client_id, body='Test',  bot_script='script_name')
    script = await Message.objects.get_last_script_bot(client_id=client_id)
    try:
        assert message.bot_script == script
    finally:
        await tx.rollback()
  
    await database.disconnect()


@pytest.mark.asyncio
async def test_get_message():
    await database.connect()
    tx = await database.transaction()
    client_id = 22
    message = await Message.objects.create(client_id=client_id, body='Test',  bot_script='script_name')
    get_message = await Message.objects.get_message(message_id=message.id)
    try:
        assert get_message.id == message.id
    finally:
        await tx.rollback()
  
    await database.disconnect()

