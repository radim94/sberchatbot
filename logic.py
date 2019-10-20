import re
import os
from utils import read_message_from_txt, write_message_to_txt
from integrations import get_server_info, set_new_as_version, reload_process_or_server, \
    clear_temp, subscribe_on_push, get_pr_or_commits_info





#======================================================================================================================
#логгирование
import logging
import datetime

s = str(datetime.datetime.now())[:19]#создаём имя логгера в зависимости от текущей даты-времени и кладём в папку логов
s = re.sub('-', '_', s)# чтобы при правках и новом запуске сервера старый лог не затирался
s = re.sub(':', '_', s)
s = re.sub(' ', '__', s)
logger_name = s
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=os.path.join(os.getcwd(), 'logs', logger_name),
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

s0 = """Здравствуйте! Я тестовый чат-бот ChatOps на API SberChat. Я позволяю получать информацию о состоянии сервера, установок релизов и управлять DevOps трубой через SberChat.
Если вы хотите получить информацию о состоянии сервера(uptime, запущенные процессы, статистика использования ресурсов, и т.д.), введите '1'. Если вы хотите выполнить административные действия на сервере(установка новой версии АС, перезапуск процессов/сервера, очистка temp директорий, и т.д.), введите '2'.
Если вы хотите подписаться на уведомления о статусе сборки, результатах выполнения тестов, результате установки АС и т.п., то введите '3'. Если вы хотите получить информацию о наличии новых commit/pull request в GIT и запустить сборщик релиза на указанном commit/pull request, введите '4'."""
s1 = "Здесь будет выводиться информация о состоянии сервера(uptime, запущенные процессы, статистика использования ресурсов, и т.д.)."
s2 ="Если вы хотите установить новую версию АС, введите '1'. Если вы хотите сделать перезапуск процессов/сервера, введите '2'. Если вы хотите очистить temp директории, введите '3'."
s3 = """Вы успешно подписаны на уведомления о статусе сборки, результатах выполнения тестов, результате установки АС и т.п."""
s4 = '''Здесь будет логика по получению информации о наличии новых commit/pull request в GIT и запустить сборщик релиза на указанном commit/pull request. Введите любую фразу или 'назад' для продолжения, 'нет' для выхода.'''
s5 = "Здесь будет логика по установке новой версии АС. "
s6 = "Здесь будет логика по перезапуску процессов/сервера"
s7 = "Здесь будет логика по очистке temp-директорий"


d3 = \
        {0: s0,
         1: s1,
         2: s2,
         3: s3,
         4: s4,
         5: s5,
         6: s6,
         7: s7}

graph_weights3 = \
        {0: [1, 1, 1, 1, 1, 0, 0, 0],
         1: [1, 1, 0, 0, 0, 0, 0, 0],
         2: [1, 0, 1, 0, 0, 1, 1, 1],
         3: [1, 0, 0, 0, 0, 0, 0, 0],
         4: [1, 0, 0, 0, 0, 0, 0, 0],
         5: [1, 0, 1, 0, 0, 0, 0, 0],
         6: [1, 0, 1, 0, 0, 0, 0, 0],
         7: [1, 0, 1, 0, 0, 0, 0, 0]
         }


graph3 = \
        {0: [0, 1, 2, 3, 4],
         1: [0, 1],
         2: [0, 2, 5, 6, 7],
         3: [0],
         4: [0],
         5: [0],
         6: [0, 2]}

########################################################################################################################
########################################################################################################################
#                                          2 BOT PART

good_words = ['да']
bad_words = ['нет']
back_words = ['назад']


def read_state_from_chat_by_id(user_id):
    return read_message_from_txt(user_id)


def write_to_chat_by_id(user_id, message, state):
    write_message_to_txt(user_id, message, state)


def predict_state(user_id, message_from_user):
    mess, state = read_state_from_chat_by_id(user_id)
    mess = message_from_user
    replic = 'Начальная'
    one_state = True
    # переменная-флаг, для того,чтобы делать только один переход из одного состояния в другое
    message = mess
    # получаем сообщение от пользователя
    if (state == 0) & one_state:
        # из нулевого состояния можем перейти в состояния 0,1,2
        one_state = False
        if message == '1':
            # переход из нулевого состояния в состояние 1
            state = 1
            replic = d3[state]
        elif message == '2':
            # переход из нулевого состояния в состояние 2
            state = 2
            replic = d3[state]
        elif message == '3':
            # переход из нулевого состояния в состояние 3
            state = 3
            replic = d3[state]
        elif message == '4':
            # переход из нулевого состояния в состояние 4
            state = 4
            replic = d3[state]
        else:
            # переход из нулевого состояния в состояние 0
            state = 0
            replic = d3[state]
    if (state == 1) & one_state:
        # из первого состояния можем перейти в состояния 0,3,4
        one_state = False
        if message in back_words:
            # переход из первого состояния в состояние 0
            state = 0
            replic = d3[state]
        elif message in bad_words:
            # переход из второго состояния в состояние 0
            state = 0
            replic = d3[state]
        else:
            # переход из первого состояния в состояние 1
            state = 1
            get_server_info(message)# тут будет какая-то логика по выводу информации о состоянии сервера(uptime, запущенные процессы, статистика использования ресурсов, и т.д.).
            replic = d3[state]
    if (state == 2) & one_state:
        # из второго состояния можем перейти в состояния 0,5,6
        one_state = False
        if message in back_words:
            # переход из второго состояния в состояние 0
            state = 0
            replic = d3[state]
        elif message in bad_words:
            # переход из второго состояния в состояние 0
            state = 0
            replic = d3[state]
        elif message == '1':
            # переход из второго состояния в состояние 5
            state = 5
            replic = d3[state]
        elif message == '2':
            # переход из второго состояния в состояние 6
            state = 6
            replic = d3[state]
        elif message == '3':
            # переход из второго состояния в состояние 7
            state = 7
            replic = d3[state]
        else:
            # переход из второго состояния в состояние 2
            state = 2
            replic = d3[state]
    if (state == 3) & one_state:
        subscribe_on_push(message)
        # здесь будет логика по очистке временных директорий
        # из третьего состояния можем перейти в состояния 0
        state = 0
        replic = d3[state]
    if (state == 4) & one_state:
        get_pr_or_commits_info(message)
        # здесь будет логика по получению инфы о коммитах и пр
        # из четвёртого состояния можем перейти в состояния 0
        state = 0
        # переход в нулевое состояние
        replic = d3[state]
    if (state == 5) & one_state:
        set_new_as_version(message) # здесь будет логика по установке новой версии ас
        # из пятого состояния можем перейти в состояния 0
        if message in back_words:
            # переход из второго состояния в состояние 2
            state = 2
            replic = d3[state]
        else:
            state = 0
            # переход в нулевое состояние
            replic = d3[state]
    if (state == 6) & one_state:
        reload_process_or_server(message) # здесь будет логика по перезагрузке процессов на сервере
        # из шестого состояния можем перейти в состояния 0 - фиктивное состояние для будущего расширения функционала
        if message in back_words:
            # переход из второго состояния в состояние 2
            state = 2
            replic = d3[state]
        else:
            state = 0
            # переход в нулевое состояние
            replic = d3[state]
    if (state == 7) & one_state:
        clear_temp(message)  # здесь будет логика по очистке
        # из седьмого состояния можем перейти в состояния 0 - фиктивное состояние для будущего расширения функционала
        if message in back_words:
            # переход из второго состояния в состояние 2
            state = 2
            replic = d3[state]
        else:
            state = 0
            # переход в нулевое состояние
            replic = d3[state]
    if replic == 'Начальная':
        if message in back_words:
            # переход из второго состояния в состояние 2
            state = 2
            replic = d3[state]
        else:
            state = 0
            # переход в нулевое состояние
            replic = d3[state]
    print(replic)
    print(state)
    write_to_chat_by_id(user_id, replic, state)
    return replic, state




########################################################################################################################
########################################################################################################################

