import schemas
from models import Message

async def create_bot_message(body, **kwargs):
    return await create(
        body=body,
        bot_script=kwargs.get('script_name'),
        with_bot = True
    )

async def create(
        body: str,
        bot_script,
        **kwargs,
) -> schemas.Message:
    data = {
        'body': body,
        'bot_script': bot_script,
        'client_id': kwargs.get('client_id')
    }

    message = await Message.objects.create(**data)
    return schemas.Message.from_orm(message)