from fastapi import FastAPI
from pydantic import BaseModel
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

def check_new_message():
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM messages')
    count = cur.fetchone()
    return count

@app.get('/check_message')
async def check_message():
    count = check_new_message()
    return {"count": count}

@app.post('/post_message')
async def post_message(message: Message):
    new_message_register(message)
    return("Maybe good")

init_db()