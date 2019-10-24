from dialog_api import peers_pb2
from dialog_bot_sdk.bot import DialogBot
import grpc
from enum import Enum
from jira.exceptions import JIRAError
import os
from dialog_bot_sdk import interactive_media
from collections import defaultdict
from text_commands import load_answer_functions, get_answer

from jira_api.logic import JIRA_UI
from jira_api.test_jira import JIRA_API

user_data = {
    'server': 'http://172.30.18.111:8080',
    'login': '1',
    'password': '1'
}


class State(Enum):

    SHOW_SPRINT = 1
    SHOW_MY_TASKS = 2
    SHOW_TASK = 3


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

    # print(params[0])
    # user = users_state.setdefault(params[0].peer.id, User(**user_data))
    # if user.state != State.SHOW_TASK:
    #     user.task_id = None
    message = params[0].message.textMessage.text.lower()
    answer = get_answer(message, params[0].peer.id)
    bot.messaging.send_message(
        bot.users.get_user_outpeer_by_id(params[0].peer.id),
        answer.text
    )
    if message in ['посмотреть спринт', 'show sprint']:
        user.state = State.SHOW_SPRINT
        options = user.jira.get_issues_in_sprint()
        bot.messaging.send_message(
            bot.users.get_user_outpeer_by_id(params[0].peer.id),
            f'В спринте {len(options)} задач. Для просмотра задачи выберите её в выпадающем списке внизу',
            JIRA_UI.show_issues_in_sprint(options)
        )
    elif message.startswith('assign'):
        if user.state == State.SHOW_TASK:
            ms = message.split()
            if len(ms) >= 2:
                whom = ms[1]
            else:
                whom = 'me'
            if whom == 'me':
                result = user.jira.assign_issue(user.task_id)
            else:
                try:
                    result = user.jira.assign_issue(user.task_id, whom)
                except JIRAError:
                    result = False
            if not result:
                bot.messaging.send_message(
                    bot.users.get_user_outpeer_by_id(params[0].peer.id),
                    f'Вы неправильно указали nickname, кому назначить задачу.'
                )
            else:
                bot.messaging.send_message(
                    bot.users.get_user_outpeer_by_id(params[0].peer.id),
                    f'Задача {user.task_id} назначена пользователю {whom}'
                )
        else:
            bot.messaging.send_message(
                bot.users.get_user_outpeer_by_id(params[0].peer.id),
                f'Вы не выбрали задачу.'
            )
    elif message.startswith('transition'):
        if user.state == State.SHOW_TASK:
            ms = message.split()
            if len(ms) >= 2:
                transition_id = " ".join(ms[1:])
            else:
                bot.messaging.send_message(
                    bot.users.get_user_outpeer_by_id(params[0].peer.id),
                    f'Вы должны ввести id или name для статуса.'
                )
                return
            transition_name = user.jira.transition_issue(transition_id, user.task_id)
            bot.messaging.send_message(
                bot.users.get_user_outpeer_by_id(params[0].peer.id),
                f'Задача {user.task_id} переведена в статус {transition_name}.'
            )
        else:
            bot.messaging.send_message(
                bot.users.get_user_outpeer_by_id(params[0].peer.id),
                f'Вы не выбрали задачу.'
            )


def on_click(*params):
    # print('on click', params)
    # # print(users_state)
    action = params[0].id
    user = users_state.get(params[0].uid)
    assert user is not None, 'u_state is None'
    if action == 'select_task_in_sprint':
        user.state = State.SHOW_TASK
        user.task_id = params[0].value
        task_id = params[0].value
        task_data = user.jira.get_issue_info(task_id)
        transition = user.jira.get_issue_transition(task_id)
        transition_str = ''
        options = user.jira.get_issues_in_sprint()
        for id_, name in transition.items():
            transition_str += f'id={id_}, name="{name}"\n'
        bot.messaging.send_message(
            bot.users.get_user_outpeer_by_id(params[0].uid),
            f'Task: {task_data["key"]}\n'
            f'Summary: {task_data["summary"]}\n'
            f'Description: {task_data["description"]}\n'
            f'Status: {task_data["status"]}\n\n'
            f'Для назначения задачи на себе введите assign me\n'
            f'Для назначения задачи на другого пользователя введите assign <nickname>\n'
            f'Для изменения статуса задачи введите команду transition <id or name>.\n'
            f'Доступные значения для id, name:\n'
            f'{transition_str}\n'
            f'Выбрать задачу:',
            JIRA_UI.show_issues_in_sprint(options)
        )
    elif action == 'select_task':
        user.state = State.SHOW_TASK
        user.task_id = params[0].value
        task_id = params[0].value
        task_data = user.jira.get_issue_info(task_id)
        transition = user.jira.get_issue_transition(task_id)
        transition_str = ''
        options = user.jira.get_issues_in_sprint()
        for id_, name in transition.items():
            transition_str += f'id={id_}, name="{name}"\n'
        bot.messaging.send_message(
            bot.users.get_user_outpeer_by_id(params[0].uid),
            f'Task: {task_data["key"]}\n'
            f'Summary: {task_data["summary"]}\n'
            f'Description: {task_data["description"]}\n'
            f'Status: {task_data["status"]}\n\n'
            f'Для назначения задачи на другого пользователя введите assign <nickname>\n'
            f'Для изменения статуса задачи введите команду transition <id or name>.\n'
            f'Доступные значения для id, name:\n'
            f'{transition_str}\n'
            f'Выбрать задачу:',
            JIRA_UI.show_issues(options)
        )


if __name__ == '__main__':
    load_answer_functions()
    bot = DialogBot.get_secure_bot(
        'hackathon-mob.transmit.im:443',
        grpc.ssl_channel_credentials(),
        '86020643997976086d7cc80db129b4c1d4a0542c'
    )
    bot.messaging.on_message(on_msg1, on_click)
