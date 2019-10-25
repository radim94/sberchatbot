from src.model.prometheus import Alert


class AlertWrapper(object):
    """
        Prometheus AlertMessage + user id list for maijling
    """

    def __init__(self, alert:Alert=None, user_id_list=[], **entries):
        self.alert = alert
        self.user_id_list = user_id_list
        self.__dict__.update(entries)
