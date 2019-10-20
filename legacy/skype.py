#======================================================================================================================
#====================================== ������ ���������,�������� ���������� ==========================================

#from sr import just_speech_recognition
import uuid
from flask import Flask, request, abort,jsonify
import requests
import json
import re
import logging
import os
from legacy.logic import predict_state,logger_name
import legacy.bot_properties as bp

#####################################################
skype_bot_code,skype_bot_password,webhook,trello_user_KEY,trello_user_token,trello_user_board_id,jira_user,jira_password,jira_server,trello_list,jira_project=bp.read_properties()


#####################################################


app = Flask(__name__)
app.config['UPLOAD_PATH'] = ''
# ��������� ������ ��� ����� ���������, ��������, ���������  � �.�.
#message=''
#context=''
#state=0
#final_dialog=0
#confidence=1
#id='megabot'

#������ ���� Microsoft Bot Framework
CLIENT_ID = skype_bot_code#"c558e163-0fc0-410e-afff-cc6f7a4868fc"
CLIENT_SECRET = skype_bot_password #"firOBBV2-~;@efcoGKX9653"


path_to_chats = os.path.join(os.getcwd(), 'chats') #os.path.join(os.getcwd(), 'chats') # path_to_chats = os.path.join(path_to_files, 'chats')
path_to_logs = os.path.join(os.getcwd(), 'logs')
########################################################################################################################
#======================================================================================================================
#������������
import logging
import datetime
#import re
#s=str(datetime.datetime.now())[:19]#������ ��� ������� � ����������� �� ������� ����-������� � ����� � ����� �����
#s=re.sub('-','_',s)# ����� ��� ������� � ����� ������� ������� ������ ��� �� ���������
#s=re.sub(':','_',s)
#s=re.sub(' ','__',s)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=logger_name,#os.path.join(os.getcwd(),'logs',s),
                    filemode='w')
# Until here logs only to file: 'logs_file'

# define a new Handler to log to console as well
console = logging.StreamHandler()
# optional, set the logging level
console.setLevel(logging.INFO)
# set a format which is the same for console use
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

# Now, we can log to both ti file and console
#logging.info('Jackdaws love my big sphinx of quartz.')
#logging.info('Hello world')
#=======================================================================================================================


########################################################################################################################
########################################################################################################################
#                       2 TEXT PART(MESSAGES CONTROLLER)



def get_access_token(client_id, client_secret):
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://api.botframework.com/.default',
        'grant_type': 'client_credentials'
    }
    r = requests.post("https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token", data=payload,
                      headers={'Content-Type': 'application/x-www-form-urlencoded'})
    try:
        response = json.loads(r.text)
        return response['access_token']
    except:
        return False



def send_message_new(token, conversation_id, activity_id, data):
    URL = "https://smba.trafficmanager.net/apis/v3/conversations/%s/activities/%s" % (conversation_id,activity_id)
    logging.info(URL)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % token
    }
    #data = json.dumps(dict(message=dict(content=message))).encode()
    print(data)
    r = requests.post(URL, data=data, headers=headers)
    return r.text, r.status_code

@app.route('/', methods=['GET', 'POST'])#��� ��� ������ ���������
def main():
    return 'This a testing calling and text API(Python) server for work with ChatBotMMK and Bots Platform(Avrora, Sberbank).'

@app.route('/api/messages', methods=['GET', 'POST'])#��� ��� �������� ���������
def main_new():
    data = json.loads(request.data.decode('utf-8'))
    logging.info(data)
    message = data['text']
    conversation_id=data['conversation']['id']# id ������
    #conversation_name = data['conversation']['name']
    type=data['type']# ��� ����������(���������, ��������� ������ � �.�.)
    recipient_id=data['from']['id']#�� ���� �������� ��������� � ���� ����� ��������
    #recipient_name = data['from']['name']
    from_id=data['recipient']['id']# ��� � id ����
    from_name=data['recipient']['name']
    activity_id=data['id']# id ����������(���������, ���������� ������ � �.�.)
    answer=handler(message,recipient_id)#,recipient_id#'����!����� ����� ������ �� ��������� �����'#handle_dialog(message)
    print(answer)
    msg = {
    "type": type,
    "from": {
        "id": from_id,
        "name": from_name
    },
    "conversation": {
        "id": conversation_id#,
       # "name": conversation_name
   },
   "recipient": {
        "id": recipient_id#,
        #"name": recipient_name
    },
    "text": answer,
    "replyToId": activity_id
    }
    print(data)
    data = json.dumps(msg)

    TOKEN = get_access_token(CLIENT_ID, CLIENT_SECRET)
    logging.info(TOKEN)
    if TOKEN:
        logging.info(send_message_new(TOKEN, conversation_id, activity_id, data))
    return '���������������'


def handler(message,user_id):
    user_id=''.join(re.findall("[a-zA-Z0-9]+",user_id))
    context=''
    message_1,state=read_message_from_txt(user_id)
    print('message in handler= '+message+" state in handler= "+str(state)+' for user '+user_id)
    answer, state = predict_state(message, state, context)
    print('message in handler after predict = ' + message + " state in handler after predict = " + str(state)+' for user '+user_id)
    write_message_to_txt(user_id,message,state)
    return answer

########################################################################################################################
########################################################################################################################
#                                           3 ��������������� �������

def read_message_from_txt(user_id):
    separator = "="
    keys = {}
    filename = str(user_id) + ".txt"
    logging.info(filename)


    path_to_mess1 = os.path.join(path_to_chats, filename)


    #with open(path_to_mess,'rw',encoding='utf-8') as f:
    if os.path.exists(path_to_mess1):
        logging.info('Read file '+path_to_mess1)
        with open (path_to_mess1,'r',encoding='utf-8') as f:
            #f.seek(0, 0)
            for line in f:
                logging.info('line='+line)
                if separator in line:
                # Find the name and value by splitting the string
                    name, value = line.split(separator, 1)
                    name=''.join(re.findall("[a-z]+",name))

                # Assign key value pair to dict
                # strip() removes white space from the ends of strings
                    keys[name.strip()] = value.strip()
            message=str(keys['message'])
            state=int(keys['state'])
            logging.info('message='+message)
            logging.info("We read from file "+filename+ " message="+message+" state="+str(state))

    else:
        with open (path_to_mess1,'w',encoding='utf-8') as f:
            logging.info('Create file with name= '+path_to_mess1+'.txt')
            message = ''
            state=0
            f.write('message=' + message+'\nstate='+str(state))  # ���������� ��� ��� � ���������� � ����� ����
            logging.info("We write to file "+path_to_mess1+" message="+message+" state="+str(state))
            #pass#f.seek(0, 0)

    return message, state




def write_message_to_txt(user_id, message:str, state:str):
    logging.info('Write_message for user '+str(user_id))
    logging.info('message for writing='+message+' for user '+str(user_id))
    logging.info('state for writing='+str(state)+' for user '+str(user_id))
    filename = str(user_id) + ".txt"
    path_to_mess1 = os.path.join(path_to_chats, filename)
    with open(path_to_mess1, 'w',encoding="utf-8") as file_2: # ����  � ��� ������ �����
        file_2.write('message='+message+'\nstate='+str(state)) # ���������� ��� ��� � ���������� � ����� ����



########################################################################################################################
########################################################################################################################
#                                                                MAIN
#TODO ��������� �� WSGI
#app.run(port=9090)
if __name__ == '__main__':
    #app.run()
    app.run(port=9095)
#app.run()