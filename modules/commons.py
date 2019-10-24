def answer_menu(args, answer):
    answer.buttons = ({"value": "button_one", "label": "button_one"},
                      {"value": "button_two", "label": "button_two"})


def answer_help(args, answer):
    answer.text = "Я умный супермегабот. Набирай команды, постараюсь выполнить :=]"


def answer_unknown(args, answer):
    answer.text = "Не понял, чего тебе надо?"


