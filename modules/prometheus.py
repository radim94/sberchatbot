from src.model.prometheus.Metric import PrometheusLabels
from src.model.prometheus.UserFilters import AlertmanagerUserFilter
from src.prometheus.prometheus_logic import PrometheusLogicService


def answer_prometheus(args, answer, credentials):
    answer.text = '''
    metrics <HOST> -- show selected host metrics
    alerts -- show alert
    subscribe <HOST> -- subscribe alert notification by host
    unsubscribe <HOST> -- unsubscribe alert notification by host
    subscription -- get subscription list
    prometheus -- print this help
    '''


def answer_metrics(args, answer, credentials):
    metrics = PrometheusLogicService.get_host_list()
    if len(args) != 1:
        answer.text = " Get host metrics"
        answer.selects = ({('metrics ' + host): host for index, host in enumerate(metrics)}, 'Choose host')
    if len(args) == 1:
        answer.text = str(PrometheusLogicService.get_host_status(args[0]))
    return answer


def answer_alerts(args, answer, credentials):
    alerts = PrometheusLogicService.get_alert_list()
    answer.text = "Alerts: \n"
    answer.text += "\n".join(list(set([str(alert) for alert in alerts])))
    return answer


def answer_subscribe(args, answer, credentials):
    metrics = PrometheusLogicService.get_host_list()
    if len(args) != 1:
        answer.text = "Choose host to subscribe on alerts"
        answer.selects = ({('subscribe ' + host): host for index, host in enumerate(metrics)}, 'Choose host')
    elif len(args) == 1:
        AlertmanagerUserFilter.update_or_create(user_id=credentials['user_id'], label=PrometheusLabels.INSTANCE,
                                                include_value=args[0])
        answer.text = 'subscription success'
    return answer


def answer_unsubscribe(args, answer, credentials):
    metrics = PrometheusLogicService.get_host_list()
    if len(args) != 1:
        answer.text = "Choose host to subscribe on alerts"
        answer.selects = ({('subscribe ' + host): host for index, host in enumerate(metrics)}, 'Choose host')
    elif len(args) == 1:
        AlertmanagerUserFilter.del_label_value(user_id=credentials['user_id'], label=PrometheusLabels.INSTANCE,
                                               include_value=args[0])
        answer.text = 'unsubscription success'
    return answer


def answer_subscription(args, answer, credentials):
    answer.text = "\n".join([x.get_text_message() for x in list(
        AlertmanagerUserFilter.query(AlertmanagerUserFilter.user_id == credentials['user_id']))])
