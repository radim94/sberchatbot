from flask import Flask, request, jsonify
"""
Тестовый рест-серви для получения алертов
"""



app = Flask(__name__)


@app.route('/', methods=['POST'])
def alert1():
    """
    Получени alert от alertmanager
    :return:
    """

    alert = request.json


    print(alert)
    pass

@app.route('/alert', methods=['POST'])
def alert():
    """
    Получени alert от alertmanager
    :return:
    """

    alert = request.json


    print(alert)
    pass

if __name__ == "__main__":
    app.run(port=7777)
