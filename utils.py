import os
import logging
import re

path_to_chats = os.path.join(os.getcwd(), 'chats') #os.path.join(os.getcwd(), 'chats') # path_to_chats = os.path.join(path_to_files, 'chats')
path_to_logs = os.path.join(os.getcwd(), 'logs')

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