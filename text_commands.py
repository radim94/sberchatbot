import importlib
import inspect
import math
import os
import sys
import traceback


class Answer:
    text = None
    buttons = dict()  # ({value: "", label: ""})
    selects = tuple()


def get_credentials(user_id):
    return {
        'login': '1',
        'password': '1'
    }


def get_answer(message, user_id):
    credentials = get_credentials(user_id)
    return do_command(message, credentials)


commands = []
answer_functions = dict()
ANSWER_PREFIX = 'answer_'
COMMAND_UNKNOWN = 'unknown'


def load_answer_functions_from_module(module):
    for name, obj in inspect.getmembers(module):
        if name.startswith('__') and name.endswith('__'):
            continue
        if inspect.isclass(obj):
            load_answer_functions_from_module(obj)
        elif inspect.ismethod(obj) or inspect.isfunction(obj):
            if name.startswith(ANSWER_PREFIX):
                answer_functions[name] = obj
                commands.append(name[len(ANSWER_PREFIX):])


def load_answer_functions():
    module_dir = 'modules'
    for root, dirs, files in os.walk(module_dir):
        for file in files:
            if file.endswith('.py'):
                load_answer_functions_from_module(importlib.import_module(module_dir + '.' + file[:-3]))


def distance(a, b):
    # "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def do_command(message, credentials):
    params = message.split()
    command = find_command(params[0])
    args = list(params)[1:]

    answer = Answer()

    function_name = ANSWER_PREFIX + command
    try:
        answer_function = answer_functions[function_name]
        answer_function(args, answer, credentials)
    except Exception as e:
        answer.text = 'ERROR'
        print('Call for {} failed'.format(function_name))
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)

    return answer


def find_command(command):
    lcommand = command.lower()
    max_dist = int(math.log2(len(lcommand)))
    for cmd_name in commands:
        if distance(cmd_name, lcommand) <= max_dist:
            return cmd_name
    return COMMAND_UNKNOWN
