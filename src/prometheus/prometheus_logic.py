from src.model.prometheus.Metric import ServerLabels, ServerMetrics, HostStatus
from src.model.prometheus.UserFilters import AlertmanagerUserFilter
from src.prometheus.prometheus_service import PrometheusService
from src.utils.lists import get_first_or_def, get_num_or_def


class PrometheusLogicService():
    """
    Логика для работы с сервисами прометеуса
    1. Подписка на alert, отписка
    2. Получение списка серваков
    3. ПОлучение метрик по стенду

    """

    base_label_config = {
        "job": "node"
    }

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def get_host_list(cls):
        return PrometheusService.get_label_values(ServerLabels.INSTANCE)

    @classmethod
    def get_host_status(cls, instance: str):
        """

        :param instance:
        :return: HostStatus
        """
        status_dict = dict()
        status_dict["uptime (days)"] = PrometheusService.get_uptime(instance)

        for metric in [x for x in ServerMetrics.get_list() if "__" not in x]:
            label_config = {**cls.base_label_config, **{ServerLabels.INSTANCE: instance}}
            metric_res_list = PrometheusService.get_metric_value(metric, label_config)
            value = get_num_or_def(get_first_or_def(metric_res_list, dict()).get('value', []), None, 1)
            if value is not None:
                status_dict[metric] = value

        return HostStatus(instance, **status_dict)

    @classmethod
    def get_alert_list(cls,labels=dict()):
        label_config = {**cls.base_label_config, **labels}
        return PrometheusService.get_alerts(label_config)


        return []

class AlertSubscService():

    @classmethod
    def subscribe_to_alert(cls, user_id: int, label, include_value: str):
        filters = AlertmanagerUserFilter.query(
            AlertmanagerUserFilter.user_id == user_id)
        filters = list(filters)

        filters = [x for x in filters if x.label == label]
        if len(filters) > 0:
            filt = filters[0]

            filt = AlertmanagerUserFilter.load(filt.id)

            filt.include_values.add(include_value)

            if (include_value in filt.exclude_values):
                filt.exclude_values.remove(include_value)

            filt.save()

    @classmethod
    def unsubscribe_to_alert(cls, user_id: int, label, value: str):
        filters = AlertmanagerUserFilter.query(
            AlertmanagerUserFilter.user_id == user_id)
        filters = list(filters)

        filters = [x for x in filters if x.label == label]
        if len(filters) > 0:
            filt = filters[0]

            filt = AlertmanagerUserFilter.load(filt.id)

            filt.include_values.remove(value)
            #
            # if (value in filt.exclude_values):
            #     filt.exclude_values.remove(value)

            filt.save()


if __name__ == "__main__":
    # AlertSubscService.subscribe_to_alert(1489, ServerLabels.INSTANCE, "localhost:9100")
    #
    # fl = list(AlertmanagerUserFilter.all())
    #
    # print(fl)
    # for f in fl:
    #     print(f._data)
    #
    # AlertSubscService.unsubscribe_to_alert(1489, ServerLabels.INSTANCE, "localhost:9100")
    #
    # fl = list(AlertmanagerUserFilter.all())
    #
    # print(fl)
    # for f in fl:
    #     print(f._data)

    # print(PrometheusLogicService.get_host_status("localhost:9100"))


    print(PrometheusLogicService.get_alert_list({ServerLabels.INSTANCE: "localhost:9100"}))
