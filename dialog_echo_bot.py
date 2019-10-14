from dialog_bot_sdk.bot import DialogBot
import grpc
import os


def on_msg(*params):
    print('on msg', params)
    bot.messaging.send_message(
        params[0].peer, 'Reply to : ' + str(params[0].message.textMessage.text)
    )


if __name__ == '__main__':


    bot = DialogBot.get_secure_bot(
        'hackathon-mob.transmit.im:443',
        grpc.ssl_channel_credentials(),
        os.environ.get('BOT_TOKEN')
    )
    bot.messaging.on_message(on_msg)
