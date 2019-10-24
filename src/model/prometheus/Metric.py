import prometheus_api_client

from enum import Enum


class ServerLabels:
    INSTANCE = 'instance'


class ServerMetrics(dict):
    """Метрики для вывода конечному пользователю"""
    metrics = ['up',
               'instance:node_cpu_utilization:ratio',
               'instance:node_filesystem_free:fs_used_percents'
               ]

    @classmethod
    def get_list(cls):
        return cls.metrics;


class PrometheusLabels:
    INSTANCE = 'instance'
    JOB = 'job'


if __name__ == "__main__":
    print(ServerMetrics['up'])
    # prom = prometheus_api_client.PrometheusConnect()
    #
    # my_label_config = {ServerLabels.INSTANCE: "localhost:9100"}
    #
    # # metric_data = prom.get_metric_range_data(metric_name='up', label_config=my_label_config)
    #
    # # a = prom.get_current_metric_value("(time() - process_start_time_seconds) / 86400", label_config=my_label_config)
    # a = prom.custom_query("(time() - process_start_time_seconds) / 86400")
    # print(a)
    pass
