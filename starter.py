from collections import defaultdict

import grpc
from dialog_bot_sdk import interactive_media
from dialog_bot_sdk.bot import DialogBot

from text_commands import load_answer_functions, do_command, get_credentials, set_credentials


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


user_states=defaultdict(int)

def on_message(msg_):
    user, message = get_user_message(msg_)
    state = user_states[user.id]

    # choise = get_choise(message, state)
    if user_states[user.id]==1:
        set_credentials(user.id,message.split()[0],message.split()[1])
        user_states[user.id] == 0
    try:
        credentials = get_credentials(user.id)
        if credentials is None:
            bot.messaging.send_message(user, 'input login and password (space separated)')
            user_states[user.id]=1
            return
        answer = do_command(message,credentials=credentials)

        group = []
        if answer.selects:
            group.append(add_interactive(answer.selects[1], answer.selects[0], type_='select'))
        group.extend([add_interactive(button['label'], button['value']) for button in answer.buttons])

        answer_text = answer.text
        if answer_text is None or len(answer_text) == 0 or answer_text == " ":
            answer_text = ' '
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
    BITBUCKET_SERVER = "http://172.30.18.187:7990"
    load_answer_functions()
    bot = DialogBot.get_secure_bot(
        'hackathon-mob.transmit.im:443',
        grpc.ssl_channel_credentials(),
        '86020643997976086d7cc80db129b4c1d4a0542c'
    )
    # print(bot.users.get_user_full_profile_by_nick('asavt'))
    bot.messaging.on_message(on_message, on_message)
