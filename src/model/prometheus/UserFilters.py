from walrus import *

from src.utils.lists import get_first_or_def

db = Database(host='172.30.18.111')


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

    @classmethod
    def update_or_create(cls, user_id, label, include_value=None, exclude_value=None):
        lst = list(AlertmanagerUserFilter.query(AlertmanagerUserFilter.user_id == user_id))
        lst = [x for x in lst if x.label == label]

        if len(lst) > 0:
            alert_filter = get_first_or_def(lst)
            alert_filter = AlertmanagerUserFilter.load(alert_filter.id)
            alert_filter.include_values.add(include_value)
            alert_filter.save()
        else:
            AlertmanagerUserFilter.create(user_id=user_id,label=label,include_value=set(include_value)) #TODO excledues


    @classmethod
    def del_label_value(cls,user_id, label, include_value=None,):
        lst = list(AlertmanagerUserFilter.query(AlertmanagerUserFilter.user_id == user_id))
        lst = [x for x in lst if x.label == label]

        if len(lst) > 0:
            alert_filter = get_first_or_def(lst)
            alert_filter = AlertmanagerUserFilter.load(alert_filter.id)
            alert_filter.include_values.remove(include_value)
            alert_filter.save()
        else:
            pass

    def get_text_message(self):
        return self.label + " : " + str(self.include_values)
