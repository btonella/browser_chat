from flask import Flask, request, redirect, session, render_template
import pika
import os
import threading
import asyncio

from src.database import *
from src.rabbitmq import *
from src.encrypt import *
from src.messages import Messages


app = Flask(__name__)
app.secret_key = 'secret'
app.config['RABBIT_MQ_URL'] = config.get('RABBIT_MQ_URL')
app.config['EXCHANGE_NAME'] = 'chat'


@app.route('/', methods=['GET'])
def main():
    if "logged_user" not in session or session["logged_user"] is None:
        return redirect("/login")

    chat = Messages().get_messages()
    # print('chat: '+str(chat))
    return render_template('main.html', user=session["logged_user"], chat=chat)


@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@app.route('/signin', methods=['GET'])
@app.route('/login')
def login():
    return render_template('signin.html')


@app.route("/auth", methods=["POST", ])
def auth():
    if (request.form["username"] is None or request.form["password"] is None):
        return redirect("/signin")

    conn = open_connection()
    user = get_user(conn, request.form["username"], request.form["password"])
    close_connection(conn)
    if (user != False and user != None):
        session["logged_user"] = request.form["username"]
        return redirect("/")
    else:
        return redirect('/')


@app.route("/create", methods=["POST", ])
def create():
    if (request.form["username"] is None or request.form["password"] is None):
        return redirect("/signin")

    conn = open_connection()
    encrypted_password = encrypt_password(request.form["password"])
    user = save_user(conn, request.form["username"], encrypted_password)
    close_connection(conn)
    if (user != False):
        session["logged_user"] = request.form["username"]
        return redirect("/")


@app.route("/logout")
def logout():
    session["logged_user"] = None
    return redirect("/")


@app.route('/send', methods=['POST', ])
def send():
    text = request.form['message']
    resp = add_chat_message(text, session['logged_user'])
    if (isinstance(resp, tuple) and resp[0] == True):
        print('message save: '+str(resp[1]))
    elif (isinstance(resp, tuple) and resp[0] == False):
        print('message error')
    elif (isinstance(resp, str)):
        # is stock
        Messages().save_message(resp)
    else:
        print('message error')

    return redirect('/')


if __name__ == '__main__':

    print("services running, press ctrl+c to stop")
    try:
        print("starting thread Rabbit")
        thread = threading.Thread(target=waitRabbitMessage)
        thread.daemon = True
        thread.start()

        print("starting Flask")
        app.run()

    except KeyboardInterrupt:
        exit(0)
