from jira_api.test_jira import JIRA_API
from jira.exceptions import JIRAError


def get_jira_obj(credentials):
    return JIRA_API(server='http://172.30.18.111:8080',
                    **credentials)


def answer_tasks(args, answer, credentials):
    jira = get_jira_obj(credentials)
    if not args:
        options = jira.get_assigned_issue()
        answer.text = f'У вас {len(options)} задач. Для просмотра задачи выберите её в выпадающем списке внизу',
        answer.select = (options, 'Tasks')
        return
    else:
        task_key = args[1]
        task_data = jira.get_issue_info(task_key)
        transition = jira.get_issue_transition(task_key)
        transition_str = ''
        options = jira.get_assigned_issue()
        for id_, name in transition.items():
            transition_str += f'id={id_}, name="{name}"\n'
        answer.text = (f'Task: {task_data["key"]}\n'
                       f'Summary: {task_data["summary"]}\n'
                       f'Description: {task_data["description"]}\n'
                       f'Status: {task_data["status"]}\n\n'
                       f'Для назначения задачи на другого пользователя введите assign <nickname>\n'
                       f'Для изменения статуса задачи введите команду transition <id or name>.\n'
                       f'Доступные значения для id, name:\n'
                       f'{transition_str}\n'
                       f'Выбрать задачу:')
        answer.select = (options, 'Tasks')


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

