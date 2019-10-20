import trello
import requests
import json
import bot_properties as bp
#FIXME numberous,repeated import, odd parameters in different modules,files


skype_bot_code,skype_bot_password,webhook,trello_user_KEY,trello_user_token,trello_user_board_id,jira_user,jira_password,jira_server,trello_list,jira_project=bp.read_properties()

KEY = trello_user_KEY #key и token можно получить на api.trello
TOKEN = trello_user_token
ID = trello_user_board_id

def trello_main():
    client = trello.TrelloClient(api_key=KEY, token=TOKEN)
    board = client.get_board(ID)

    all_boards = client.list_boards()  # получим тестовую и рабочую доску
    # last_board = all_boards[-1]
    last_board = all_boards[5]
    last_board.list_lists()
    print(last_board.name)
    print(all_boards)
    print(last_board)

    for l in last_board.list_lists():  # получаем списки  в доске
        print(l.name)
        print(l.id)

    my_list = last_board.get_list('5b3cae9b72fc0edcee85cbf2')  # id выбираем из полученных на предыдущем шаге

    print(my_list)

    for card in my_list.list_cards():  # выводим карточки на листе
        print(card.name)



def add_card(name:str,desc=''):#метод добавляет карточку в список 'список' на тестовую доску
    data = {
        'key': KEY,
        'token': TOKEN,
        'name': name,
        'desc': desc,
        'pos': "top",
        'idList': '5b98dfc3e765317fd61e3d80'
    }
    # FIXME take list from properties
    data = json.dumps(data)
    json_1 = json.loads(data)
    print(json_1)
    uri = 'https://api.trello.com/1/cards/'
    r = requests.post(uri, json=json_1, verify=False)
    print(r.text)