from dialog_bot_sdk.bot import DialogBot
import grpc
import os
from logic import predict_state


def on_msg(*params):
    print('on msg', params)
    bot.messaging.send_message(
        params[0].peer, predict_state(params[0].peer.id, str(params[0].message.textMessage.text))[0])



if __name__ == '__main__':


    bot = DialogBot.get_secure_bot(
        'hackathon-mob.transmit.im:443',
        grpc.ssl_channel_credentials(),
        os.environ.get('BOT_TOKEN')
    )
    bot.messaging.on_message(on_msg)
