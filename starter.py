from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint

from dialog_api import peers_pb2
from dialog_bot_sdk.bot import DialogBot
import grpc
import os
from dialog_bot_sdk import interactive_media
from stashy.pullrequests import PullRequest

from bitbucket_Api.common_bb import *
from text_commands import find_command, load_answer_functions, COMMAND_UNKNOWN, do_command

user_states = defaultdict(State)


def get_init_message(state):
    message = ''
    if state.project is not None:
        message += f'selected project:{state.project}\n'
    if state.repository is not None:
        message += f'selected repository:{state.repository}\n'
    if state.pull_request is not None:
        message += f'selected pull request:{state.pull_request}\n'

    # message += '1:select project\n'
    message_int = [add_interactive('project', "select project")]

    # message += '2: select PR\n'
    message_int.append(add_interactive('PR', 'select PR'))

    if state.project is not None:
        # message += '3: select repository\n'
        message_int.append(add_interactive("repo", 'select repository'))

    if state.pull_request is not None:
        # message += f'4: manage selected pull request \n'
        message_int.append(add_interactive('manage_PR', 'manage selected PR'))

    message += '0: exit\n'
    message_int.append(add_interactive('exit', 'exit'))

    return message, message_int


def add_interactive(media_id, text, type_='button'):
    if type_ == 'button':
        return interactive_media.InteractiveMedia(
            media_id,
            interactive_media.InteractiveMediaButton(str(media_id), text)
        )
    if type_ == 'list' or type_ == 'select':
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
    if state.step == Steps.INIT:
        answer, int_answer = get_init_message(state)
        state.step = Steps.START
    elif state.step == Steps.START:
        if choise == 'project':
            state.step = Steps.PROJECT_LIST
            pl = project_list()
            state.project_list = pl
            answer = " "
            int_answer = [
                add_interactive('Projects',
                                {str(index + 1): proj['key'] for index, proj in enumerate(pl)},
                                type_='list'),
                add_interactive('back', 'back')
            ]

        if choise == 'PR':
            state.step = Steps.MANAGE_PR_OPTIONS
            prs = [pr for pr in PR_list() if pr['state'] == 'OPEN']
            state.pr_list = prs
            answer = ' '
            int_answer = [add_interactive('PRs',
                                          {str(index + 1): proj['title'] for index, proj in enumerate(prs)},
                                          type_='list'),
                          add_interactive('back', 'back')
                          ]
        if choise == 'manage_PR':
            state.step = Steps.MANAGE_PR_OPTIONS
            return get_message_state(state, 'skip')
        if choise == 'repo':
            state.step = Steps.REPO_LIST
            pl = repo_list(state.project)
            state.repo_list = pl
            answer = ' '
            int_answer = [add_interactive('Repos',
                                          {str(index + 1): proj['slug'] for index, proj in enumerate(pl)},
                                          type_='list'),
                          add_interactive('back', 'back')
                          ]
        if choise == 'exit':
            state = State()
            answer = ' '
            int_answer = []
            return get_message_state(state, choise)
    elif state.step == Steps.MANAGE_PR_OPTIONS:
        if choise != 'back' and choise != 'skip':
            choise = int(choise)

            if choise > 0 and choise <= len(state.pr_list):
                pr = state.pr_list[choise - 1]
            state.repository = pr['fromRef']['repository']['slug']
            state.project = pr['fromRef']['repository']['project']['key']
            state.pull_request = pr['id']
        elif choise == 'back':
            state.step = Steps.INIT
            return get_message_state(state, choise)
        state.step = Steps.MANAGE_PR
        ans = [
            'approve',
            'decline',
            'merge',
            'unapprove',
            'get comment',
            'get linked jira task',
            'get commits',
            'back'
        ]

        answer = '\n'.join(str(index + 1) + ' : ' + pr for index, pr in enumerate(ans))
        answer = ' '
        int_answer = [add_interactive(proj, proj) for index, proj in enumerate(ans)]

        can_merge = stash.projects[state.project].repos[state.repository].pull_requests[state.pull_request].can_merge()
        if can_merge:
            answer = f'PR can be merged\n' + answer
    elif state.step == Steps.MANAGE_PR:
        pr: PullRequest
        pr = stash.projects[state.project].repos[state.repository].pull_requests[state.pull_request]
        print(choise)
        if choise == 'approve':
            pr.approve()
        elif choise == 'decline':
            pr.decline()
        elif choise == 'merge':
            stash.projects[state.project].repos[state.repository].pull_requests[state.pull_request].merge(version=0)
        elif choise == 'unapprove':
            pr.unapprove()
        elif choise == 'get comment':
            return state, '\n'.join(
                x['comment']['author']['name'] + ':' + x['comment']['text'] for x in pr.activities() if
                x['action'] == 'COMMENTED'), []
        elif choise == 'get linked jira task':
            return state, '\n'.join(x['key'] + '  :  ' + x['url'] for x in pr.issues()), []
        elif choise == 'get commits':
            pprint(list(pr.commits()))
            return state, '\n'.join(x['author']['name'] + '  :  ' + x['displayId'] for x in pr.commits()), []
        else:
            state.step = Steps.START
            return get_message_state(state, 'PR')
        state.step = Steps.INIT
        return get_message_state(state, choise)
    elif state.step == Steps.PROJECT_LIST:
        if choise == 'back':
            state.step = Steps.INIT
            return get_message_state(state, choise)
        choise = int(choise)
        if int(choise) > 0 and int(choise) <= len(state.project_list):
            state.project = state.project_list[choise - 1]['key']
            state.step = Steps.INIT
            return get_message_state(state, choise)
    elif state.step == Steps.REPO_LIST:
        if choise == 'back':
            state.step = Steps.INIT
            return get_message_state(state, choise)

        choise = int(choise)
        if int(choise) > 0 and int(choise) <= len(state.project_list):
            state.repository = state.repo_list[choise - 1]['slug']
            state.step = Steps.INIT
            return get_message_state(state, choise)

    else:
        return get_message_state(state, choise)

    return state, answer, [interactive_media.InteractiveMediaGroup(int_answer)]


def on_message(msg_):
    user, message = get_user_message(msg_)
    # state = user_states[user.id]

    # choise = get_choise(message, state)

    try:
        command = find_command(message)
        if command !=COMMAND_UNKNOWN:
            answer = do_command(command)

        group=[]
        if answer.selects is not None:
            group.append(add_interactive(answer.selects[1], answer.selects[0], type_='select'))
        group.extend([add_interactive(button['label'],button['value']) for button in answer.buttons])

        answer_text=answer.text
        if answer_text is None or len(answer_text)==0 or answer_text==" ":
            answer_text=' '
        if len(group) != 0:
            interactive_answer = [interactive_media.InteractiveMediaGroup(group)]
            bot.messaging.send_message(user, answer_text, interactive_answer)
        else:
            bot.messaging.send_message(user, answer_text)

    except Exception as e:
        print(e)
        bot.messaging.send_message(user, 'ERROR')
        raise e

    # bot.messaging.send_message(user, '<a href="http://172.30.18.111:8080/browse/TEST-1">')


if __name__ == '__main__':
    load_answer_functions()
    bot = DialogBot.get_secure_bot(
        'hackathon-mob.transmit.im:443',
        grpc.ssl_channel_credentials(),
        'c9c60f2d3ff65c01c4ca0ed340c1ea64d110af8a'
    )
    # print(bot.users.get_user_full_profile_by_nick('asavt'))
    bot.messaging.on_message(on_message, on_message)
