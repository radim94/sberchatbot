import re
from legacy.trello_c import add_card
import os
from legacy.jira_c import add_task_jira
import legacy.bot_properties as bp

#FIXME numberous,repeated import, odd parameters in different modules,files


skype_bot_code,skype_bot_password,webhook,trello_user_KEY,trello_user_token,trello_user_board_id,jira_user,jira_password,jira_server,trello_list,jira_project=bp.read_properties()


#======================================================================================================================
#логгирование
import logging
import datetime
#import re
s=str(datetime.datetime.now())[:19]#создаём имя логгера в зависимости от текущей даты-времени и кладём в папку логов
s=re.sub('-','_',s)# чтобы при правках и новом запуске сервера старый лог не затирался
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

s0 = """Здравствуйте! Я тестовый бот по добавлению задач в JIRA и Trello. Куда Вы хотите добавить задачу? Введите TRELLO или JIRA для продолжения."""
s1 = "Пожалуйста, введите название карточки для задачи в Trello. Введите 'назад' или 'нет' для возвращения назад."
s2 ="Пожалуйста, введите данные по задаче в JIRA. Введите 'назад' или 'нет' для возвращения назад."
s3 = """Карточка успешно добавлена в Trello! Вы можете найти Вашу карточку по адресу https://trello.com/b/wdHQ0R0P/skypetrellobot на доске SkypeTrelloBot в листе 'список'. Ваша карточка должна быть наверху списка. Введите любую фразу или символ для продолжения или выхода."""
s4 = '''Извините, у меня не получилось добавить задачу в Trello, попробуйте исправить ошибки и повторить ещё раз. Введите любую фразу или 'назад' для продолжения, 'нет' для выхода.'''
#s5 = "Задача успешно добавлена в JIRA. Вы можете найти результат работы по адресу https://sbtatlas.sigma.sbrf.ru/jira/secure/RapidBoard.jspa?rapidView=8224 в неназначенных задачах. Введите любую фразу или символ для продолжения или выхода."
s5 = "Задача успешно добавлена в JIRA. Вы можете найти результат работы по адресу " +jira_server+'/projects/'+jira_project+" . Для входа введите логин= "+jira_user+" пароль= "+ jira_password+' .'
s6 = "Извините, у меня не получилось добавить задачу в JIRA, попробуйте исправить ошибки и повторить ещё раз. Введите любую фразу или 'назад' для продолжения, 'нет' для выхода."


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
good_words=['да']
bad_words=['нет']
back_words=['назад']



def predict_state(mess,state,context):
    replic='Начальная'
    one_state=True# переменная-флаг, для того,чтобы делать только один переход из одного состояния в другое
    message=mess# получаем сообщение от пользователя
    if ((state==0) & one_state):# из нулевого состояния можем перейти в состояния 0,1,2
        one_state=False
        if (message =='TRELLO'): #переход из нулевого состояния в состояние 1
            state=1
            replic=d3[state]
        elif (message == 'JIRA'): #переход из нулевого состояния в состояние 2
            state=2
            replic=d3[state]
        else: #переход из нулевого состояния в состояние 0
            state=0
            replic=d3[state]
    if ((state==1) & one_state): #из первого состояния можем перейти в состояния 0,3,4
        one_state=False
        if (message in back_words): #переход из первого состояния в состояние 0
            state=0
            replic=d3[state]
        elif (message in bad_words): #переход из второго состояния в состояние 0
            state=0
            replic=d3[state]
        else: #переход из первого состояния в состояние 3
            state=3
            add_card(message)# добавляем карточку в Trello
            replic=d3[state]
    if ((state==2) & one_state): #из второго состояния можем перейти в состояния 0,5,6
        one_state=False
        if (message in back_words): #переход из второго состояния в состояние 0
            state=0
            replic=d3[state]
        elif (message in bad_words): #переход из второго состояния в состояние 0
            state=0
            replic=d3[state]
        else: # переход из второго состояния в состояние 5
            state=5
            add_task_jira(message)
            replic=d3[state]
    if ((state==3) & one_state): # из третьего состояния можем перейти в состояния 0
        state=0
        replic=d3[state]
    if ((state==4) & one_state): # из четвёртого состояния можем перейти в состояния 0,1 - фиктивное состояние для будущего расширения функционала
        state=0# переход в нулевое состояние
        replic=d3[state]
    if ((state==5) & one_state): # из пятого состояния можем перейти в состояния 0
        state=0 # переход в нулевое состояние
        replic=d3[state]
    if ((state==6) & one_state): # из шестого состояния можем перейти в состояния 0,2 - фиктивное состояние для будущего расширения функционала
        state=0 # переход в нулевое состояние
        replic=d3[state]
    if replic=='Начальная':
        state=0
        replic=d3[state]
    print(replic)
    print(state)
    return replic,state




########################################################################################################################
########################################################################################################################

