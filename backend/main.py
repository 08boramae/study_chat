from fastapi import FastAPI, Form
from typing import Annotated
from pydantic import BaseModel
import json
import sqlite3

conn = sqlite3.connect('./database', check_same_thread=False)
app = FastAPI()

class Message(BaseModel):
    name: str
    message: str

def init_db():
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS messages (name TEXT, message TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT)')
    conn.commit()

def new_message_register(message: Message):
    cur = conn.cursor()
    cur.execute('INSERT INTO messages (name, message) VALUES (?, ?)', (message.name, message.message))
    conn.commit()

def check_message_count():
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM messages')
    count = cur.fetchone()
    return count

def check_message_content():
    cur = conn.cursor()
    cur.execute('SELECT * FROM messages')
    messages = cur.fetchall()
    messages_list = [{'id': msg[2], 'name': msg[0], 'message': msg[1]} for msg in messages]
    json_data = json.dumps(messages_list, ensure_ascii=False)
    print(json_data)
    return json_data

@app.get('/check_message_count')
async def check_message_new():
    count = check_message_count()
    return {"count": count}

@app.get('/check_messages')
async def check_messages():
    messages = check_message_content()
    # parsing messages to json
    return {"messages": messages}

@app.post('/post_message')
async def post_message(message: Annotated[Message, Form()]):
    try:
        new_message_register(message)
        return {"status": "200", "message": "Message posted successfully"}
    except:
        return {"status": "500", "message": "Internal Server Error"}

init_db()