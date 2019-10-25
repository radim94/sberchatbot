from src.model.prometheus.Alert import Alert
from src.model.prometheus.AlertWrapper import AlertWrapper
from src.model.prometheus.UserFilters import AlertmanagerUserFilter
from src.model.redis.User import User


class AlertService(object):
    """
    Сервис для отбработки поступивших оповещений
    """

    @classmethod
    def process_alertmanager_message(cls, alert_message):
        alerts = _get_alert_list(alert_message)

        mail_wrappers = [AlertWrapper(alert, get_user_id_list(alert)) for alert in alerts]

        for w in mail_wrappers:
            cls.__send_alert_to_users(w)

    @classmethod
    def __send_alert_to_users(cls, alert_wrapper: AlertWrapper):
        # TODO вызвать АПИ бота
        # convert
        print("processed", alert_wrapper.alert.get_text_message())
        pass


def _get_alert_list(alert_message):
    alert_list = alert_message.get("alerts", [])
    return [Alert(**x) for x in alert_list]


def _check_alert(alert: Alert, filter: AlertmanagerUserFilter):
    filter_label = filter.label
    includes = filter.include_values
    excludes = filter.exclude_values

    alert_labels = alert.labels

    if filter_label not in alert_labels:
        return True

    alert_label_value = alert_labels.get(filter_label, None)

    """ check excludes"""
    if alert_label_value in excludes:
        return False
    if alert_label_value in includes:
        return True

    return False


def check_alert(alert: Alert, filter_list: AlertmanagerUserFilter):
    """
    Проверяем prometheus alert на соответствие фильтрам
    :return: bool
    """
    for filter in filter_list:
        if not _check_alert(alert, filter):
            return False
        return True


def filter_alerts(alert_list, filter_list):
    return [x for x in alert_list if check_alert(x, filter_list)]


def get_user_id_list(alert: Alert):
    """
    :param alert:
    :return: list


    """

    user_id_list = []

    for user in User.all():
        filter_list = list(AlertmanagerUserFilter.query(AlertmanagerUserFilter.user_id == user.id))
        if check_alert(alert, filter_list):
            user_id_list.append(user.id)
    return user_id_list
