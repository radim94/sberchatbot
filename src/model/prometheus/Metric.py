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


class HostStatus():

    def __init__(self, host, **entries):
        self.host = host
        self.__dict__.update(entries)

    def to_message_string(self):
        s = "HOST: " + self.host

        d = [x for x in self.__dict__ if "__" not in x]

        for x in d:

            if x != 'host':
                s += "\n {0} : {1}".format(x, self.__dict__[x])

        return s

    def __repr__(self):
        return self.to_message_string()


