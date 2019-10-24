import prometheus_api_client

from main import config
from urllib.parse import urljoin

import requests

from src.model.prometheus.Metric import ServerLabels
from src.utils.lists import get_num_or_def, get_first_or_def


class PrometheusService():
    """
    Сервис для работы с метриками, поставляемымт Прометеусом

    """

    PROMETHEUS_HOST = config.PROMETHEUS_SERVER_HOST

    api_labels = "http://" + PROMETHEUS_HOST + "/api/v1/label/{0}/values"

    __prom = prometheus_api_client.PrometheusConnect("http://" + config.PROMETHEUS_SERVER_HOST)

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def get_metric_value(self, metric_name, labels):
        res = self.__prom.get_current_metric_value(metric_name=metric_name, label_config=labels)
        # print(res)
        # return res.get('value', [None, None])[0]
        return res

    @classmethod
    def get_alerts(self, filter):
        pass

    @classmethod
    def get_label_values(cls, label):
        resp = requests.get(cls.api_labels.format(label))
        return resp.json().get("data", [])

    @classmethod
    def get_uptime(cls, instance):
        """ Uptime (days)"""
        metric_res_list = cls.__prom.custom_query(
            "(time() - process_start_time_seconds{instance='" + instance + "'}) / 86400")
        return get_num_or_def(get_first_or_def(metric_res_list, dict()).get('value', []), None, 1)


if __name__ == "__main__":
    # print(config.PROMETHEUS_SERVER_HOST)
    # print(urljoin("http://localhost:9090/", "/api/v1/label/{0}/values"))
    # prom = prometheus_api_client.PrometheusConnect()
    #
    my_label_config = {ServerLabels.INSTANCE: "localhost:9100"}
    #
    # metric_data = prom.get_current_metric_value(metric_name='up', label_config=my_label_config)
    # print(metric_data)
    #
    # print(PrometheusService.get_label_values("instance"))

    # print(PrometheusService.get_metric_value("up", None))
    print(PrometheusService.get_uptime("localhost:9100"))

    pass
