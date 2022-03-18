import json
import time
from flask import Flask, request
from flask import render_template
from datetime import datetime
# подключение библиотеки

app = Flask(__name__)

messages = []

DB_FILE = "./data/db.json"
db = open(DB_FILE,"rb")
data  = json.load(db)
messages = data["messages"]

def save_messages_to_file():
    db = open(DB_FILE, "w")
    data = {
        "messages": messages
    }
    json.dump(data,db)

def add_messages(text, sender): # Обявим функцию которая добавит список
    """

    :param text: текст сообщения
    :param sender: отправитель
    :param time: текущее время
    """
    times = datetime.now()
    # timedtr = times.strftime("Date: %d/%m/%Y  time: %H:%M:%S")


    new_messange = {
        "text": text,
        "sender": sender,
        #"time": "23:59", # ToDO: добавить дату
        #"time": (f"{times.hour}:{times.minute}"),
        "time": times.strftime("%H:%M"),

    }
    messages.append(new_messange)

def print_massage(message): # обявляем функцию печати
    print(f"[{message['sender'] }]: {message['text']} / {message['time']}")


for message in messages:
    print_massage(message)

# Главная страница
@app.route("/")
def index_page():
    return "Здраствуйте вас приветствует скил чат"

# показать все сообщения в формате JSON
@app.route("/get_messages")
def get_messages():
    return { "messages": messages}

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/send_message")
def send_message():
    # получить
    name = request.args["name"]
    text = request.args["text"]
    # вызвать add_message
    if (101 > len(name) > 2 and 0 < len(text) < 3001):
        add_messages(text,name)
        save_messages_to_file()
        return "ok"
    else:
        return "ERROR"


app.run() # запуск сервера фласка

