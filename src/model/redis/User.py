from walrus import *

db = Database()


class User(Model):
    __database__ = db
    __namespace__ = 'user'


    id = IntegerField(primary_key=True)
    name = TextField()
    chatid = TextField()
    phone = TextField(index=True)

    is_blocked = BooleanField(default=False)

    alpha_mail = TextField()
    sigma_mail = TextField()

    alpha_login = TextField()
    sigma_login = TextField()

    bitbucket_user_id = TextField()
    jira_user_id = TextField()
    jenkins_user_id = TextField()

    # Подписка должна задаваться условиями (список метрик, стенд, джоба\любые поля)
    prometheus_subscription_list = ListField()






if __name__ == "__main__":

    usr_dct = {'id':1481,
        'name': 'test',
               # 'chatid': 'test',
               # 'phone': 'test',
               'is_blocked': False,
               'alpha_mail': 'test',
               'sigma_mail': 'test',
               'alpha_login': 'test',
               'sigma_login': 'test',
               'bitbucket_user_id': 'test',
               'jira_user_id': 'test',
               'jenkins_user_id': 'test'}
    User.create(**usr_dct)


    for user in User.all():
        print(user._data)

