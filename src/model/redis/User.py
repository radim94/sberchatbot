from walrus import *

db = Database(host='172.30.18.111')


class User(Model):
    __database__ = db
    __namespace__ = 'user'

    id = IntegerField(primary_key=True)
    name = TextField()
    chatid = TextField()
    phone = TextField(index=True)

    password = TextField()
    login = TextField()

    is_blocked = BooleanField(default=False)

    alpha_mail = TextField()
    sigma_mail = TextField()

    alpha_login = TextField()
    sigma_login = TextField()

    bitbucket_user_id = TextField()
    bitbucket_user_token = TextField()

    jira_user_id = TextField()
    jenkins_user_id = TextField()

    # Подписка должна задаваться условиями (список метрик, стенд, джоба\любые поля)
    prometheus_subscription_list = PickledField(default=set())
    alertmanaget_filters = PickledField(default=set())

