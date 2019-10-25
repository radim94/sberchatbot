from walrus import *

db = Database(host='172.30.18.111')


class Message(Model):
    """
    Базовый объект сообщения

    """

    __database__ = db
    __namespace__ = 'messages'

    id = IntegerField(primary_key=True)
    user_id = UUIDField(index=True)
    chatid = TextField()

    content = Field()

    creation_date = DateField(index=True)
