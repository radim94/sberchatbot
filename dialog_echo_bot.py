from dialog_api import peers_pb2
from dialog_bot_sdk.bot import DialogBot
import grpc
import os
from dialog_bot_sdk import interactive_media
from collections import defaultdict

from jira_api.logic import JIRA_UI
from jira_api.test_jira import JIRA_API

user_data = {
    'server': 'http://172.30.18.111:8080',
    'login': '1',
    'password': '1'
}


class User:

    def __init__(self, server, login, password):
        self.jira = JIRA_API(server, login, password)
        self.state = 'START'
        self.task_id = None


users_state = {}


def on_msg(*params):
    print('on msg', params)
    bot.messaging.send_message(
        params[0].peer, 'Reply to : ' + str(params[0].message.textMessage.text)
    )


def on_msg1(*params):
    # print(params[0].peer.id)
    user = users_state.setdefault(params[0].peer.id, User(**user_data))


    # if user.state == 'START':
    #     pass
    # bot.messaging.send_message(
    #     params[0].peer,
    #     "JIRA",
    #     JIRA_UI.get_start_buttons()
    # )


def on_click(*params):
    print('on click', params)
    # print(users_state)
    action = params[0].id
    user = users_state.get(params[0].uid)
    assert user is not None, 'u_state is None'
    if action == 'show_my_issue':
        tasks = user.jira.get_assigned_issue()
        bot.messaging.send_message(
            bot.users.get_user_outpeer_by_id(params[0].uid),
            'Tasks',
            JIRA_UI.show_issues(tasks)
        )
    elif action == 'select_task':
        task_id = params[0].value
        task_data = user.jira.get_issue_info(task_id)
        transition = user.jira.get_issue_transition(task_id)
        bot.messaging.send_message(
            bot.users.get_user_outpeer_by_id(params[0].uid),
            f'Task: {task_data["key"]}\n'
            f'Summary: {task_data["summary"]}\n'
            f'Description: {task_data["description"]}\n'
            f'Status: {task_data["status"]}\n\n'
            f'Для переназначения задачи введите команду assign <username>',
            JIRA_UI.show_transition(transition)
        )
        user.task_id = task_id
    elif action == 'transition':
        transition_id = params[0].value
        task_data = user.jira.transition_issue(transition_id, user.task_id)
        bot.messaging.send_message(
            bot.users.get_user_outpeer_by_id(params[0].uid),
            f'Task: {task_data["key"]}\n'
            f'Summary: {task_data["summary"]}\n'
            f'Description: {task_data["description"]}\n'
            f'Status: {task_data["status"]}'
        )
        user.task_id = None

    # if u_state == 'START'
    # bot.users.get_user_outpeer_by_id(params[0].uid)
    # bot.messaging.send_message(bot.users.get_user_outpeer_by_id(params[0].uid), params[0].value)


if __name__ == '__main__':
    bot = DialogBot.get_secure_bot(
        'hackathon-mob.transmit.im:443',
        grpc.ssl_channel_credentials(),
        '86020643997976086d7cc80db129b4c1d4a0542c'
    )
    # print(bot.users.get_user_full_profile_by_nick('asavt'))
    bot.messaging.on_message(on_msg1, on_click)
