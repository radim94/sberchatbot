import math
import sys
import traceback
from enum import Enum


class Answer:
    text = None
    buttons = ()  # ({value: "", label: ""})


def get_answer(message):
    return Command.do(message)


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


def answer_menu(args, answer):
    answer.buttons = ({"value": "button_one", "label": "button_one"},
                      {"value": "button_two", "label": "button_two"})


def answer_help(args, answer):
    answer.text = "Я умный супермегабот. Набирай команды, постараюсь выполнить :=]"


def answer_unknown(args, answer):
    answer.text = "Не понял, чего тебе надо?"


class Command(Enum):
    NONE = 'unknown'
    MENU = 'menu'
    HELP = 'help'

    @classmethod
    def do(cls, message):
        params = message.split()
        command = Command.find(params[0])
        args = list(params)[1:]

        answer = Answer()

        function_name = 'answer_' + command.value
        try:
            answer_function = globals()[function_name]
            answer_function(args, answer)
        except Exception as e:
            answer.text = 'ERROR'
            print('Call for {} failed'.format(function_name))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        return answer


    @classmethod
    def find(cls, command):
        lcommand = command.lower()
        max_dist = int(math.log2(len(lcommand)))
        for cmd_name in Command:
            if distance(cmd_name.value, lcommand) <= max_dist:
                return cmd_name
        return Command.NONE
