from collections import defaultdict
from dataclasses import dataclass
from enum import Enum

import grpc
from dialog_bot_sdk import interactive_media
from dialog_bot_sdk.bot import DialogBot

from src.model.prometheus.Metric import PrometheusLabels
from src.model.prometheus.UserFilters import AlertmanagerUserFilter
from src.prometheus.prometheus_logic import PrometheusLogicService


class PromSteps(Enum):
    INIT = "init"
    START = 'start'

    GET_HOST_METRICS = "GET_HOST_METRICS"
    ALERT_MAIN = "ALERT_MAIN"
    ALERT_subscribe = "ALERT_subscribe"
    ALERT_unsubscribe = "ALERT_unsubscribe"
    ALERT_GET_RULES = "ALERT_GET_RULES"
    ALERT_PUSH = "ALERT_PUSH"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, str):
            return self.value == o
        elif isinstance(o, PromSteps):
            return self.value == o.value
        else:
            return False

        return super().__eq__(o)


@dataclass
class PromState:
    host: str = None
    repository: str = None
    pull_request: str = None
    step: str = PromSteps.INIT
    user_id = None
    metrics = list()


user_states = defaultdict(PromState)


def get_init_message(state):
    message = ''
    if state.host is not None:
        message += f'selected host:{state.host}\n'

    message_int = [add_interactive('metrics', "metrics")]
    message_int.append(add_interactive('notification', "alerts"))

    message += '0: exit\n'
    message_int.append(add_interactive('exit', 'exit'))

    return message, message_int


def add_interactive(media_id, text, type_='button'):
    if type_ == 'button':
        return interactive_media.InteractiveMedia(
            media_id,
            interactive_media.InteractiveMediaButton(str(media_id), text)
        )
    if type_ == 'list':
        return interactive_media.InteractiveMedia(
            media_id,
            interactive_media.InteractiveMediaSelect(text, media_id)
        )


def get_user_message(msg):
    try:
        user = msg.peer
        message = msg.message.textMessage.text
    except Exception:
        user = bot.users.get_user_outpeer_by_id(msg.uid)
        message = str(msg.value)
    return user, message


def get_choise(message, state):
    # if message.isnumeric():
    return message
    # else:
    #     return 'unknown'


def get_message_state(state, choise):
    print('state', state)
    print('choise', choise)
    print('=' * 120)
    if state.step == PromSteps.INIT:
        answer, int_answer = get_init_message(state)
        state.step = PromSteps.START
    elif state.step == PromSteps.START:
        if choise == 'metrics':
            state.step = PromSteps.GET_HOST_METRICS

            metrics = PrometheusLogicService.get_host_list()
            state.metrics = metrics
            answer = " Get host metrics"
            int_answer = [
                add_interactive('Choose host',
                                {str(index + 1): host for index, host in enumerate(metrics)},
                                type_='list'),
                add_interactive('back', 'back')
            ]

        if choise == 'notification':
            state.step = PromSteps.ALERT_MAIN

            answer = " "
            int_answer = [
                add_interactive('get_alerts', 'get alerts'),
                add_interactive('subscribe', 'subscribe'),
                add_interactive('unsubscribe', 'unsubscribe'),
                add_interactive('subscriptions', 'subscriptions'),

                add_interactive('back', 'back')
            ]
        if choise == 'exit':
            state = PromState()
            answer = ' '
            int_answer = []
            return get_message_state(state, choise)
    elif state.step == PromSteps.GET_HOST_METRICS:
        if choise != 'back' and choise != 'skip':
            choise = int(choise)

            if choise > 0 and choise <= len(state.metrics):
                host = state.metrics[choise - 1]

                host_metrics = str(PrometheusLogicService.get_host_status(host))

        elif choise == 'back':
            state.step = PromSteps.INIT
            return get_message_state(state, choise)

        state.step = PromSteps.GET_HOST_METRICS

        answer = host_metrics

        int_answer = [
            add_interactive('Choose host',
                            {str(index + 1): host for index, host in enumerate(state.metrics)},
                            type_='list'),
            add_interactive('back', 'back')
        ]

    elif state.step == PromSteps.GET_HOST_METRICS:
        if choise != 'back' and choise != 'skip':
            choise = int(choise)

            if choise > 0 and choise <= len(state.metrics):
                host = state.metrics[choise - 1]

                host_metrics = str(PrometheusLogicService.get_host_status(host))

        elif choise == 'back':
            state.step = PromSteps.INIT
            return get_message_state(state, choise)

        state.step = PromSteps.GET_HOST_METRICS

        answer = host_metrics

        int_answer = [
            add_interactive('Choose host',
                            {str(index + 1): host for index, host in enumerate(state.metrics)},
                            type_='list'),
            add_interactive('back', 'back')
        ]

    elif state.step == PromSteps.ALERT_MAIN:
        if choise != 'back' and choise != 'skip':
            if choise == "subscribe":
                state.step = PromSteps.ALERT_subscribe

                metrics = PrometheusLogicService.get_host_list()

                answer = "Choose host to subscribe on alerts"
                int_answer = [
                    add_interactive('Choose host',
                                    {str(index + 1): host for index, host in enumerate(metrics)},
                                    type_='list'),
                    add_interactive('back', 'back')
                ]
            elif choise == "unsubscribe":
                state.step = PromSteps.ALERT_unsubscribe

                metrics = PrometheusLogicService.get_host_list()  # TODO СПисок отфильтрованный по юзеру

                answer = "Choose host to unsubscribe on alerts"
                int_answer = [
                    add_interactive('Choose host',
                                    {str(index + 1): host for index, host in enumerate(metrics)},
                                    type_='list'),
                    add_interactive('back', 'back')
                ]
                # TODO filter by user
            elif choise == "get_alerts":
                state.step = PromSteps.ALERT_MAIN

                # metrics = PrometheusLogicService.get_host_list()

                alerts = PrometheusLogicService.get_alert_list()

                answer = "Alerts: \n"
                answer += "\n".join(list(set([str(alert) for alert in alerts])))
                int_answer = [
                    add_interactive('get_alerts', 'get alerts'),
                    add_interactive('subscribe', 'subscribe'),
                    add_interactive('unsubscribe', 'unsubscribe'),
                    add_interactive('subscriptions', 'subscriptions'),
                    add_interactive('back', 'back')
                ]

            elif choise == "subscriptions":
                state.step = PromSteps.ALERT_MAIN

                answer = "Notification rules \n"
                print(state.user_id)
                answer += "\n".join([x.get_text_message() for x in list(
                    AlertmanagerUserFilter.query(AlertmanagerUserFilter.user_id == state.user_id))])

                int_answer = [
                    add_interactive('get_alerts', 'get alerts'),
                    add_interactive('subscribe', 'subscribe'),
                    add_interactive('unsubscribe', 'unsubscribe'),
                    add_interactive('subscriptions', 'subscriptions'),
                    add_interactive('back', 'back')
                ]
        elif choise == 'back':
            state.step = PromSteps.INIT
            return get_message_state(state, choise)

    elif state.step == PromSteps.ALERT_subscribe:
        if choise != 'back' and choise != 'skip':
            choise = int(choise)
            state.metrics = PrometheusLogicService.get_host_list()

            if choise > 0 and choise <= len(state.metrics):
                host = state.metrics[choise - 1]

                AlertmanagerUserFilter.update_or_create(user_id=state.user_id, label=PrometheusLabels.INSTANCE,
                                                        include_value=host)

        elif choise == 'back':
            state.step = PromSteps.INIT
            return get_message_state(state, choise)

        choise == 'notification'
        state.step = PromSteps.ALERT_MAIN

        answer = " "
        int_answer = [
            add_interactive('get_alerts', 'get alerts'),
            add_interactive('subscribe', 'subscribe'),
            add_interactive('unsubscribe', 'unsubscribe'),
            add_interactive('subscriptions', 'subscriptions'),
            add_interactive('back', 'back')
        ]

    elif state.step == PromSteps.ALERT_unsubscribe:
        if choise != 'back' and choise != 'skip':
            choise = int(choise)

            if choise > 0 and choise <= len(state.metrics):
                host = state.metrics[choise - 1]

                AlertmanagerUserFilter.del_label_value(user_id=state.user_id, label=PrometheusLabels.INSTANCE,
                                                       include_value=host)

        elif choise == 'back':
            # choise = 'notification'
            state.step = PromSteps.INIT
            return get_message_state(state, choise)

        choise == 'notification'
        state.step = PromSteps.ALERT_MAIN

        answer = " "
        int_answer = [
            add_interactive('get_alerts', 'get alerts'),
            add_interactive('subscribe', 'subscribe'),
            add_interactive('unsubscribe', 'unsubscribe'),
            add_interactive('subscriptions', 'subscriptions'),
            add_interactive('back', 'back')
        ]




    elif choise == 'back':
        state.step = PromSteps.INIT
        return get_message_state(state, choise)

        # state.step = PromSteps.GET_HOST_METRICS
        #
        # answer = str(host_metrics)
        #
        # int_answer = [
        #     add_interactive('Choose host',
        #                     {str(index + 1): host for index, host in enumerate(state.metrics)},
        #                     type_='list'),
        #     add_interactive('back', 'back')
        # ]

    # elif state.step == Steps.MANAGE_PR:
    #     pr: PullRequest
    #     pr = stash.projects[state.project].repos[state.repository].pull_requests[state.pull_request]
    #     print(choise)
    #     if choise == 'approve':
    #         pr.approve()
    #     elif choise == 'decline':
    #         pr.decline()
    #     elif choise == 'merge':
    #         stash.projects[state.project].repos[state.repository].pull_requests[state.pull_request].merge(version=0)
    #     elif choise == 'unapprove':
    #         pr.unapprove()
    #     elif choise == 'get comment':
    #         return state, '\n'.join(
    #             x['comment']['author']['name'] + ':' + x['comment']['text'] for x in pr.activities() if
    #             x['action'] == 'COMMENTED'), []
    #     elif choise == 'get linked jira task':
    #         return state, '\n'.join(x['key'] + '  :  ' + x['url'] for x in pr.issues()), []
    #     else:
    #         state.step = Steps.START
    #         return get_message_state(state, 'PR')
    #     state.step = Steps.INIT
    #     return get_message_state(state, choise)
    # elif state.step == Steps.PROJECT_LIST:
    #     if choise == 'back':
    #         state.step = Steps.INIT
    #         return get_message_state(state, choise)
    #     choise = int(choise)
    #     if int(choise) > 0 and int(choise) <= len(state.project_list):
    #         state.project = state.project_list[choise - 1]['key']
    #         state.step = Steps.INIT
    #         return get_message_state(state, choise)
    # elif state.step == Steps.REPO_LIST:
    #     if choise == 'back':
    #         state.step = Steps.INIT
    #         return get_message_state(state, choise)
    #
    #     choise = int(choise)
    #     if int(choise) > 0 and int(choise) <= len(state.project_list):
    #         state.repository = state.repo_list[choise - 1]['slug']
    #         state.step = Steps.INIT
    #         return get_message_state(state, choise)

    else:
        return get_message_state(state, choise)

    return state, answer, [interactive_media.InteractiveMediaGroup(int_answer)]


def on_message(msg_):
    user, message = get_user_message(msg_)
    state = user_states[user.id]
    state.user_id = user.id

    choise = get_choise(message, state)

    try:
        new_state, answer, interactive_answer = get_message_state(state, choise)
        user_states[user.id] = new_state
        if len(interactive_answer) != 0:
            bot.messaging.send_message(user, answer, interactive_answer)
        else:
            bot.messaging.send_message(user, answer)
    except Exception as e:
        print(e)
        bot.messaging.send_message(user, 'ERROR')
        raise e


if __name__ == '__main__':
    bot = DialogBot.get_secure_bot(
        'hackathon-mob.transmit.im:443',
        grpc.ssl_channel_credentials(),
        '498af308cc656c602d87bc0767f95a9eeb63fcf5'
    )
    # print(bot.users.get_user_full_profile_by_nick('asavt'))
    bot.messaging.on_message(on_message, on_message)
