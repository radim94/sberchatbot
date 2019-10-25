import os

from flask import Flask, request, jsonify

from src.prometheus.alertservice import AlertService
from src.utils.props import read_properties

config = read_properties()


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

    AlertService.process_alertmanager_message(alert)

    return " ok "


if __name__ == "__main__":
    app.run(port=7777)
    # config = read_properties()
