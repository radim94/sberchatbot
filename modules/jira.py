from jira_api.jira_api import JIRA_API
from jira.exceptions import JIRAError
from jira import JIRA


def get_jira_obj(credentials):
    jira = JIRA(server='http://172.30.18.111:8080',
                basic_auth=(credentials['login'], credentials['password']))
    return JIRA_API(jira)


def answer_tasks(args, answer, credentials):
    jira = get_jira_obj(credentials)
    if not args:
        options = jira.get_assigned_issue()
        answer.text = f'У вас {len(options)} задач. Для просмотра задачи выберите её в выпадающем списке внизу'
        answer.selects = (options, 'Tasks')
        return
    else:
        task_key = args[0]
        task_data = jira.get_issue_info(task_key)
        transition = jira.get_issue_transition(task_key)
        transition_str = ''
        options = jira.get_assigned_issue()
        for id_, name in transition.items():
            transition_str += f'name="{name}"\n'
        answer.text = (f'Task: {task_data["key"]}\n'
                       f'Summary: {task_data["summary"]}\n'
                       f'Description: {task_data["description"]}\n'
                       f'Status: {task_data["status"]}\n\n'
                       f'Для назначения задачи на другого пользователя введите assign <task_name> <nickname>\n'
                       f'Для изменения статуса задачи введите команду transition <name>.\n'
                       f'Доступные значения для name:\n'
                       f'{transition_str}\n'
                       f'Выбрать задачу:')
        answer.selects = (options, 'Tasks')


def answer_assign(args, answer, credentials):
    jira = get_jira_obj(credentials)
    if not args:
        answer.text = 'Вы не указали название задачи'
    else:
        if len(args) >= 2:
            task_key, whom = args[0:2]
            try:
                result = jira.assign_issue(task_key, whom)
            except JIRAError:
                result = False
        else:
            task_key = args[0]
            result = whom = jira.assign_issue(task_key)
        if not result:
            answer.text = 'Вы неправильно указали nickname, кому назначить задачу.'
            return
        else:
            answer.text = f'Задача {task_key} назначена пользователю {whom}'


def answer_transition(args, answer, credentials):
    jira = get_jira_obj(credentials)
    if not args:
        answer.text = 'Вы не указали название задачи и целевой статус'
        return
    elif len(args) == 1:
        answer.text = 'Вы не указали целевой статус'
        return
    else:
        task_key = args[0]
        status = " ".join(args[1:])
        transition_name = jira.transition_issue(status, task_key)
        answer.text = f'Задача {task_key} переведена в статус {transition_name}.'


def answer_sprint(args, answer, credentials):
    jira = get_jira_obj(credentials)
    if not args:
        options = jira.get_issues_in_sprint()
        answer.text = f'В спринте {len(options)} задач. Для просмотра задачи выберите её в выпадающем списке внизу'
        answer.selects = (options, 'Tasks')
    else:
        task_key = args[0]
        task_data = jira.get_issue_info(task_key)
        transition = jira.get_issue_transition(task_key)
        transition_str = ''
        options = jira.get_issues_in_sprint()
        for id_, name in transition.items():
            transition_str += f'name="{name}"\n'
        answer.text = (f'Task: {task_data["key"]}\n'
                       f'Summary: {task_data["summary"]}\n'
                       f'Description: {task_data["description"]}\n'
                       f'Status: {task_data["status"]}\n\n'
                       f'Для назначения задачи на себе введите assign <task_name>\n'
                       f'Для назначения задачи на другого пользователя введите assign <task_name> <nickname>\n'
                       f'Для изменения статуса задачи введите команду transition <name>.\n'
                       f'Доступные значения для name:\n'
                       f'{transition_str}\n'
                       f'Выбрать задачу:')
        answer.selects = (options, 'Tasks')


def answer_jira_help(args, answer, credentials):
    answer.text = 'sprint - Просмотреть все задачи в спринте\n' \
                  'tasks - Просмотреть мои задачи\n' \
                  'assign <task_name> - Назначить задачу на себя\n' \
                  'assign <task_name> <nickname> - Назначить задачу на пользователя <nickname>\n' \
                  'transition <task_name> <status_name> - Перевести задачу в статус <status_name>'
