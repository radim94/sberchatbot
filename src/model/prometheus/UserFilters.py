from walrus import *

db = Database()


class AlertmanagerUserFilter(Model):
    """

    include_values :: python set

    """

    __database__ = db
    __namespace__ = 'prometheus_filters'


    id = AutoIncrementField(primary_key=True)
    user_id = IntegerField(index=True)

    label = TextField(default="", index=True)
    include_values = PickledField(default=set())
    exclude_values = PickledField(default=set())




if __name__ == "__main__":

    test =  {
        # 'id':1,
        "user_id":1481,
        'label': 'instance',
        'include_values': {'localhost:9100'}
        }

    a = AlertmanagerUserFilter.create(**test)

    for user in AlertmanagerUserFilter.query(AlertmanagerUserFilter.user_id == 1489):
        print(user._data)

