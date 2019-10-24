from collections import defaultdict

import grpc
from dialog_bot_sdk import interactive_media
from dialog_bot_sdk.bot import DialogBot
from stashy.pullrequests import PullRequest

from bitbucket_Api.common_bb import *

user_states = defaultdict(State)

def get_init_message(state):
    message = ''
    if state.project is not None:
        message += f'selected project:{state.project}\n'
    if state.repository is not None:
        message += f'selected repository:{state.repository}\n'
    if state.pull_request is not None:
        message += f'selected pull request:{state.pull_request}\n'

    message += '1:select project\n'
    message_int = [add_interactive('project', "select project")]

    message += '2: select PR\n'
    message_int.append(add_interactive('PR', 'select PR'))

    if state.project is not None:
        message += '3: select repository\n'
        message_int.append(add_interactive("repo", 'select repository'))

    if state.pull_request is not None:
        message += f'manage selected pull request \n'
        message_int.append(add_interactive('manage_PR', 'manage selected PR'))

    message += '0: exit\n'
    message_int.append(add_interactive('exit', 'exit'))

    return message,message_int


def add_interactive(media_id,text):
    return interactive_media.InteractiveMedia(
        media_id,
        interactive_media.InteractiveMediaButton(str(media_id),text)
    )

def get_user_message(msg):
    try:
        user = msg.peer
        message=msg.message.textMessage.text
    except Exception:
        user = bot.users.get_user_outpeer_by_id(msg.uid)
        message =str(msg.value)
    return user,message

def get_choise(message,state):
    # if message.isnumeric():
    return message
    # else:
    #     return 'unknown'


def get_message_state(state, choise):
    print('state',state)
    print('choise', choise)
    print('='*120)
    if state.step == Steps.INIT:
        answer,int_answer = get_init_message(state)
        state.step=Steps.START
    elif state.step ==Steps.START:
        if choise == 'project':
            state.step = Steps.PROJECT_LIST
            pl = project_list()
            state.project_list = pl
            answer = '\n'.join(str(index + 1) + ' : ' + proj['key'] for index, proj in enumerate(pl))
            int_answer = [add_interactive(index + 1, proj['key']) for index, proj in enumerate(pl)]

        if choise == 'PR':
            state.step = Steps.MANAGE_PR_OPTIONS
            prs = PR_list()
            state.pr_list = prs
            answer = '\n'.join(str(index + 1) + ' : ' + pr['title'] for index, pr in enumerate(prs))
            int_answer = [add_interactive(index + 1, proj['title']) for index, proj in enumerate(prs)]
            answer+='\nback'
            int_answer.append(add_interactive('back', 'back'))
        if choise=='manage_PR':
            state.step=Steps.MANAGE_PR_OPTIONS
            return get_message_state(state, 'back')
        if choise=='repo':
            state.step = Steps.REPO_LIST
            pl = project_list()
            state.project_list = pl
            answer = '\n'.join(str(index + 1) + ' : ' + proj['key'] for index, proj in enumerate(pl))
            int_answer = [add_interactive(index + 1, proj['key']) for index, proj in enumerate(pl)]

    elif state.step == Steps.MANAGE_PR_OPTIONS:
        if choise!='back':
            choise = int(choise)

            if choise > 0 and choise <= len(state.pr_list):
                pr=state.pr_list[choise - 1]
            state.repository = pr['fromRef']['repository']['slug']
            state.project = pr['fromRef']['repository']['project']['key']
            state.pull_request = pr['id']
        elif choise=='back':
            return get_message_state(state,choise)
        state.step = Steps.MANAGE_PR
        ans=[
            'approve',
            'decline',
            'merge',
            'unapprove',
            'back'
        ]

        answer = '\n'.join(str(index + 1) + ' : ' + pr for index, pr in enumerate(ans))
        int_answer = [add_interactive(proj, proj) for index, proj in enumerate(ans)]

        can_merge=stash.projects[state.project].repos[state.repository].pull_requests[state.pull_request].can_merge()
        if can_merge:
            answer=f'PR can be merged\n'+answer

    elif state.step == Steps.PROJECT_LIST:
        choise=int(choise)
        if int(choise) > 0 and int(choise) <= len(state.project_list):
            state.project = state.project_list[choise - 1]['key']
            state.step = Steps.INIT
            return get_message_state(state,choise)
    elif state.step == Steps.MANAGE_PR:
        pr:PullRequest
        pr=stash.projects[state.project].repos[state.repository].pull_requests[state.pull_request]
        print(choise)
        if choise =='approve':
            pr.approve()
        if choise =='decline':
            pr.decline()
        if choise =='merge':
            stash.projects[state.project].repos[state.repository].pull_requests[state.pull_request].merge(version=0)
        if choise =='unapprove':
            pr.unapprove()
        else:
            state.step=Steps.START
            return get_message_state(state, 'PR')
        state.step = Steps.INIT
        return get_message_state(state, choise)
    else:
        return get_message_state(state, choise)

    return state,answer,[interactive_media.InteractiveMediaGroup(int_answer)]


def on_message(msg_):
    user, message=get_user_message(msg_)
    state = user_states[user.id]

    choise=get_choise(message,state)

    try:
        new_state,answer,interactive_answer = get_message_state(state,choise)
        user_states[user.id] = new_state
        bot.messaging.send_message(user, answer, interactive_answer)
    except Exception as e:
        print(e)
        bot.messaging.send_message(user, 'ERROR')



    # bot.messaging.send_message(user, '<a href="http://172.30.18.111:8080/browse/TEST-1">')


if __name__ == '__main__':

    bot = DialogBot.get_secure_bot(
        'hackathon-mob.transmit.im:443',
        grpc.ssl_channel_credentials(),
        'c9c60f2d3ff65c01c4ca0ed340c1ea64d110af8a'
    )
    # print(bot.users.get_user_full_profile_by_nick('asavt'))
    bot.messaging.on_message(on_message,on_message)