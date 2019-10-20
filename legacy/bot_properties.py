import os

#FIXME logging
#FIXME если нет каких-то свойств, или файла пропертей





def read_properties():
    # default_propeties
    skype_bot_code = "c558e163-0fc0-410e-afff-cc6f7a4868fc"
    skype_bot_password = "firOBBV2-~;@efcoGKX9653"
    webhook = 'https://sbtbot.northeurope.cloudapp.azure.com:9095/'  # где вертится бот
    trello_user_KEY = 'a2a49143e4ebfd3346be3d047f7ef34f'
    trello_user_token = '9ea596df0912afac351015e4e9d3832ae9f4a4b717a824490c514dc7e7428d83'
    trello_user_board_id = 'wdHQ0R0P'
    jira_user = 'user'  # '14691412'
    jira_password = '1085607qwerty'  # '@L1a6a08!#'
    jira_server = 'http://168.63.44.17:9090'  # 'http://sbtatlas.sbrf.ru/jira'
    trello_list=''
    jira_project='TESTBOARD'#'SBERPAY'
    #####################################################################

    separator = "="
    keys = {}
    filename ="bots.properties"
    #############################################


    path_to_mess1 = filename


    #with open(path_to_mess,'rw',encoding='utf-8') as f:
    if os.path.exists(path_to_mess1):
        with open (path_to_mess1,'r',encoding='utf-8') as f:
            #f.seek(0, 0)
            for line in f:
                #logging.info('line='+line)
                if separator in line:
                # Find the name and value by splitting the string
                    name, value = line.split(separator, 1)
                    #name=''.join(rfindall("[a-z]+",name))

                # Assign key value pair to dict
                # strip() removes white space from the ends of strings
                    keys[name.strip()] = value.strip()
            skype_bot_code = str(keys['skype_bot_code'])
            skype_bot_password = str(keys['skype_bot_password'])
            webhook = str(keys['webhook'])
            trello_user_KEY = str(keys['trello_user_KEY'])
            trello_user_token = str(keys['trello_user_token'])
            trello_user_board_id = str(keys['trello_user_board_id'])
            jira_user = str(keys['jira_user'])
            jira_password = str(keys['jira_password'])
            jira_server = str(keys['jira_server'])
            jira_project = str(keys['jira_project'])
            trello_list = str(keys['trello_list'])
            #logging.info('message='+message)
            print("We read next properties: skype_bot_code="+skype_bot_code+ " skype_bot_password="+skype_bot_password+" webhook="+webhook)
            print("We read next properties: trello_user_KEY=" + trello_user_KEY + " trello_user_token=" + trello_user_token + " trello_user_board_id=" + trello_user_board_id)
            print("We read next properties: jira_user=" + jira_user + " jira_password=" + jira_password + " jira_server=" + jira_server)
            print("We read next properties: trello_list=" + jira_user + " jira_project=" + jira_project + " trello_list=" + trello_list)



    return skype_bot_code,skype_bot_password,webhook,trello_user_KEY,trello_user_token,trello_user_board_id,jira_user,jira_password,jira_server,trello_list,jira_project