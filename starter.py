import grpc
from dialog_bot_sdk import interactive_media
from dialog_bot_sdk.bot import DialogBot

from text_commands import find_command, load_answer_functions, COMMAND_UNKNOWN, do_command, get_credentials


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


def on_message(msg_):
    user, message = get_user_message(msg_)
    # state = user_states[user.id]

    # choise = get_choise(message, state)

    try:
        answer = do_command(message,credentials=get_credentials(user.id))

        group = []
        if answer.selects is not None and answer.selects!=():
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
        'c9c60f2d3ff65c01c4ca0ed340c1ea64d110af8a'
    )
    # print(bot.users.get_user_full_profile_by_nick('asavt'))
    bot.messaging.on_message(on_message, on_message)
