from text_commands import set_credentials


def answer_menu(args, answer, credentials):
    answer.buttons = ({"value": "button_one", "label": "button_one"},
                      {"value": "button_two", "label": "button_two"})


def answer_help(args, answer, credentials):
    answer.text = "Я умный супермегабот. Набирай команды, постараюсь выполнить :=]"


def answer_unknown(args, answer, credentials):
    answer.text = "Не понял, чего тебе надо?"


def answer_select(args, answer):
    answer.selects = ({'tasks TEST-8': 'TEST-8'}, "Tasks")

def answer_credentials(args,answer,credentials):
    if len(args)!=2:
        answer.text='use credentials <login>  <password> '
    else:
        set_credentials(credentials['user_id'], args[0], args[1])
        answer.text='password changed'
