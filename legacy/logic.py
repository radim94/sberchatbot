import re
from legacy.trello_c import add_card
import os
from legacy.jira_c import add_task_jira
import legacy.bot_properties as bp

#FIXME numberous,repeated import, odd parameters in different modules,files


skype_bot_code,skype_bot_password,webhook,trello_user_KEY,trello_user_token,trello_user_board_id,jira_user,jira_password,jira_server,trello_list,jira_project=bp.read_properties()


#======================================================================================================================
#������������
import logging
import datetime
#import re
s=str(datetime.datetime.now())[:19]#������ ��� ������� � ����������� �� ������� ����-������� � ����� � ����� �����
s=re.sub('-','_',s)# ����� ��� ������� � ����� ������� ������� ������ ��� �� ���������
s=re.sub(':','_',s)
s=re.sub(' ','__',s)
logger_name=s
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=os.path.join(os.getcwd(),'logs',logger_name),
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

#=======================================================================================================================

########################################################################################################################
########################################################################################################################
#                                        1 GRAPH PART

s0 = """������������! � �������� ��� �� ���������� ����� � JIRA � Trello. ���� �� ������ �������� ������? ������� TRELLO ��� JIRA ��� �����������."""
s1 = "����������, ������� �������� �������� ��� ������ � Trello. ������� '�����' ��� '���' ��� ����������� �����."
s2 ="����������, ������� ������ �� ������ � JIRA. ������� '�����' ��� '���' ��� ����������� �����."
s3 = """�������� ������� ��������� � Trello! �� ������ ����� ���� �������� �� ������ https://trello.com/b/wdHQ0R0P/skypetrellobot �� ����� SkypeTrelloBot � ����� '������'. ���� �������� ������ ���� ������� ������. ������� ����� ����� ��� ������ ��� ����������� ��� ������."""
s4 = '''��������, � ���� �� ���������� �������� ������ � Trello, ���������� ��������� ������ � ��������� ��� ���. ������� ����� ����� ��� '�����' ��� �����������, '���' ��� ������.'''
#s5 = "������ ������� ��������� � JIRA. �� ������ ����� ��������� ������ �� ������ https://sbtatlas.sigma.sbrf.ru/jira/secure/RapidBoard.jspa?rapidView=8224 � ������������� �������. ������� ����� ����� ��� ������ ��� ����������� ��� ������."
s5 = "������ ������� ��������� � JIRA. �� ������ ����� ��������� ������ �� ������ " +jira_server+'/projects/'+jira_project+" . ��� ����� ������� �����= "+jira_user+" ������= "+ jira_password+' .'
s6 = "��������, � ���� �� ���������� �������� ������ � JIRA, ���������� ��������� ������ � ��������� ��� ���. ������� ����� ����� ��� '�����' ��� �����������, '���' ��� ������."


d3={0:s0,1:s1,2:s2,3:s3,4:s4,5:s5,6:s6}

graph_weights3 = {0: [1,1,1,0,0,0,0],
         1: [1,0,0,1,1,0,0],
         2: [1,0,0,0,0,1,1],
         3: [1,0,0,0,0,0,0],
         4:[1,1,0,0,0,0,0],
         5:[1,0,0,0,0,0,0],
         6:[1,0,1,0,0,0,0],
         }


graph3 = {0: [0,1,2],
         1: [0,3,4],
         2: [0,3,4],
         3: [0],
         4:[0,1],
         5:[0],
         6:[0,2]}

########################################################################################################################
########################################################################################################################
#                                          2 BOT PART

platform=['TRELLO','JIRA']
good_words=['��']
bad_words=['���']
back_words=['�����']



def predict_state(mess,state,context):
    replic='���������'
    one_state=True# ����������-����, ��� ����,����� ������ ������ ���� ������� �� ������ ��������� � ������
    message=mess# �������� ��������� �� ������������
    if ((state==0) & one_state):# �� �������� ��������� ����� ������� � ��������� 0,1,2
        one_state=False
        if (message =='TRELLO'): #������� �� �������� ��������� � ��������� 1
            state=1
            replic=d3[state]
        elif (message == 'JIRA'): #������� �� �������� ��������� � ��������� 2
            state=2
            replic=d3[state]
        else: #������� �� �������� ��������� � ��������� 0
            state=0
            replic=d3[state]
    if ((state==1) & one_state): #�� ������� ��������� ����� ������� � ��������� 0,3,4
        one_state=False
        if (message in back_words): #������� �� ������� ��������� � ��������� 0
            state=0
            replic=d3[state]
        elif (message in bad_words): #������� �� ������� ��������� � ��������� 0
            state=0
            replic=d3[state]
        else: #������� �� ������� ��������� � ��������� 3
            state=3
            add_card(message)# ��������� �������� � Trello
            replic=d3[state]
    if ((state==2) & one_state): #�� ������� ��������� ����� ������� � ��������� 0,5,6
        one_state=False
        if (message in back_words): #������� �� ������� ��������� � ��������� 0
            state=0
            replic=d3[state]
        elif (message in bad_words): #������� �� ������� ��������� � ��������� 0
            state=0
            replic=d3[state]
        else: # ������� �� ������� ��������� � ��������� 5
            state=5
            add_task_jira(message)
            replic=d3[state]
    if ((state==3) & one_state): # �� �������� ��������� ����� ������� � ��������� 0
        state=0
        replic=d3[state]
    if ((state==4) & one_state): # �� ��������� ��������� ����� ������� � ��������� 0,1 - ��������� ��������� ��� �������� ���������� �����������
        state=0# ������� � ������� ���������
        replic=d3[state]
    if ((state==5) & one_state): # �� ������ ��������� ����� ������� � ��������� 0
        state=0 # ������� � ������� ���������
        replic=d3[state]
    if ((state==6) & one_state): # �� ������� ��������� ����� ������� � ��������� 0,2 - ��������� ��������� ��� �������� ���������� �����������
        state=0 # ������� � ������� ���������
        replic=d3[state]
    if replic=='���������':
        state=0
        replic=d3[state]
    print(replic)
    print(state)
    return replic,state




########################################################################################################################
########################################################################################################################

