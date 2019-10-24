from dialog_api import peers_pb2
from dialog_bot_sdk.bot import DialogBot
import grpc
import os
from dialog_bot_sdk import interactive_media

def on_msg(*params):
    print('on msg', params)
    bot.messaging.send_message(
        params[0].peer, 'Reply to : ' + str(params[0].message.textMessage.text)
    )


def on_msg1(*params):
    # print('on msg', params)

    bot.messaging.send_message(
        params[0].peer,
        "buttons",
        [interactive_media.InteractiveMediaGroup(
            [
                interactive_media.InteractiveMedia(
                    1,
                    interactive_media.InteractiveMediaButton("button_one", "button_one")
                ),
                interactive_media.InteractiveMedia(
                    1,
                    interactive_media.InteractiveMediaButton("button_two", "button_two")
                ),
            ]
        )]
    )

def on_click(*params):
    print('on click', params)
    # bot.users.get_user_outpeer_by_id(params[0].uid)
    bot.messaging.send_message(bot.users.get_user_outpeer_by_id(params[0].uid),params[0].value)


if __name__ == '__main__':


    bot = DialogBot.get_secure_bot(
        'hackathon-mob.transmit.im:443',
        grpc.ssl_channel_credentials(),
        '4cf0cac139f012b7d45c95fb603a15f8a965c21a'
    )
    # print(bot.users.get_user_full_profile_by_nick('asavt'))
    bot.messaging.on_message(on_msg1,on_click)
