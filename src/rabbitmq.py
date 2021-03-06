from .messages import Messages
import json
from retry import retry
from .api import *
from .config import config
import pika
from datetime import datetime

connection = None

# CONSUME MESSAGE - CHAT 0
@retry((pika.exceptions.AMQPConnectionError, pika.exceptions.ConnectionClosed, KeyError), tries=5, delay=1)
def waitRabbitMessage():

    global connection
    try:
        # connect with rabbit
        if (connection is None):
            parameters = pika.URLParameters(config.get('RABBIT_MQ_URL'))
            connection = pika.BlockingConnection(parameters)

        channel = connection.channel()

        channel.exchange_declare(
            exchange="chat", exchange_type="fanout", durable=True)
        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='chat', queue=queue_name)
        print('[x] Listening RabbitMQ ')

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()

    except (pika.exceptions.AMQPConnectionError, pika.exceptions.ConnectionClosed, KeyError) as e:
        print('Rabbitmq connection expired')
        connection = None
        raise e


# CONSUME MESSAGE - CHAT 1
@retry((pika.exceptions.AMQPConnectionError, pika.exceptions.ConnectionClosed, KeyError), tries=5, delay=1)
def waitRabbitMessage_chat1():

    global connection
    try:
        # connect with rabbit
        if (connection is None):
            parameters = pika.URLParameters(config.get('RABBIT_MQ_URL'))
            connection = pika.BlockingConnection(parameters)

        channel = connection.channel()

        channel.exchange_declare(
            exchange="chat1", exchange_type="fanout", durable=True)
        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='chat1', queue=queue_name)
        print('[x] Listening RabbitMQ ')

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback1, auto_ack=True)
        channel.start_consuming()

    except (pika.exceptions.AMQPConnectionError, pika.exceptions.ConnectionClosed, KeyError) as e:
        print('Rabbitmq connection expired')
        connection = None
        raise e



def callback(ch, method, properties, body):
    send_back = []
    print("[x] Message from RabbitMQ - chat0:", body)

    body_ = body.decode("utf8")
    # print('body: ', body_)

    if (not isinstance(body_, list)):
        body_ = [body_]
    for item in body_:
        send_back.append(item)

    # print("send_back", send_back)
    Messages().save_message(send_back)


def callback1(ch, method, properties, body):
    send_back = []
    print("[x] Message from RabbitMQ - chat1:", body)

    body_ = body.decode("utf8")

    if (not isinstance(body_, list)):
        body_ = [body_]
    for item in body_:
        send_back.append(item)

    Messages().save_message(send_back, chat=1)


def add_chat_message(text, user, chat_name='chat'):
    finished = False
    now = str(datetime.now())[:19]
    if ('/stock=' in text):
        stock_key = text
        stock_key = stock_key.replace('/stock=', '')
        resp = find_stock(stock_key)
        if (resp == False):
            return False
        return f'{now} STOCK_BOT: {resp}'
    elif ('/' in text):
        return f'{now} STOCK_BOT: Invalid command'
    
    else:
        body = f'{now} {user}: {text}'
        try:
            parameters = pika.URLParameters(config.get('RABBIT_MQ_URL'))
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue=chat_name, durable=True)
            channel.basic_publish(
                exchange=chat_name,
                routing_key=chat_name,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ))
            connection.close()
            finished = True
        except Exception as e:
            print(e)
        finally:
            return (finished, body)
        
