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





if __name__ == "__main__":
    alertd = {
        "status": "firing",
        "labels": {
            "alertname": "DiskSpace70%Free",
            "device": "/dev/sda2",
            "fstype": "ext4",
            "instance": "localhost:9100",
            "job": "node",
            "mountpoint": "/",
            "severity": "Warning"
        },
        "annotations": {
            "description": "localhost:9100  has only 0.6754930465486997% free.",
            "summary": "Instance1 localhost:9100 is low on disk space"
        },
        "startsAt": "2019-10-24T08:12:17.832992086Z",
        "endsAt": "0001-01-01T00:00:00Z",
        "generatorURL": "http://localhost.localdomain:9090/graph?g0.expr=%28%28node_filesystem_free_bytes%7Bjob%3D%22node%22%7D+%2F+node_filesystem_size_bytes%7Bjob%3D%22node%22%7D%29%29+%3C%3D+1&g0.tab=1",
        "fingerprint": "7671fb50eef06974"
    }

    alertd1 = {
        "status": "firing",
        "labels": {
            "alertname": "DiskSpace70%Free",
            "device": "/dev/sda2",
            "fstype": "ext4",
            "instance": "NOT",
            "job": "node",
            "mountpoint": "/",
            "severity": "Warning"
        },
        "annotations": {
            "description": "localhost:9100  has only 0.6754930465486997% free.",
            "summary": "Instance1 localhost:9100 is low on disk space"
        },
        "startsAt": "2019-10-24T08:12:17.832992086Z",
        "endsAt": "0001-01-01T00:00:00Z",
        "generatorURL": "http://localhost.localdomain:9090/graph?g0.expr=%28%28node_filesystem_free_bytes%7Bjob%3D%22node%22%7D+%2F+node_filesystem_size_bytes%7Bjob%3D%22node%22%7D%29%29+%3C%3D+1&g0.tab=1",
        "fingerprint": "7671fb50eef06974"
    }

    alert = Alert(**alertd)
    alert1 = Alert(**alertd1)

    a = (get_user_id_list(alert))
    print(a)
    print(filter_alerts([alert, alert1], list(AlertmanagerUserFilter.query(AlertmanagerUserFilter.user_id == 1489))))
