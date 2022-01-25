import pytest
from httpx import AsyncClient

from async_tasks import async_tasks
from database import redis, database, database_feedback_slave
from main import app
from models import Client, Message


@pytest.mark.asyncio
async def test_chat2desk_webhook_available():
    await redis.connect()
    await database.connect()
    await database_feedback_slave.connect()
    await async_tasks.connect()

    tx = await database.transaction()

    client = await Client.objects.create(phone='4345456745', card_number='1234123412341234')

    try:
        async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
            response = await ac.post('/chat2desk/webhook', json={
                'hook_type': 'outbox',
                'type': 'to_client',
                'transport': 'external',
                'message_id': 12312,
                'client': {
                    'phone': '+74345456745',
                },
                'text': 'TEST MESSAGE',
            })
        assert response.status_code == 200
        assert response.json() == {'status': 'success'}

        actual_messages = await Message.objects.get_list(client_id=client.id, limit=4000)
        assert len(actual_messages) == 1
        assert actual_messages[0].body == 'TEST MESSAGE'

    finally:
        await tx.rollback()
    await redis.disconnect()
    await database.disconnect()
    await database_feedback_slave.disconnect()
    await async_tasks.disconnect()
