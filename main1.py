#!/bin/env python
from app import create_app,socketio,login_manager
app = create_app(debug=True)
from flask import request, session
from flask_socketio import send, emit, disconnect, rooms
from flask_login import current_user
from botocore.exceptions import ClientError
import functools, boto3,time
from app.main.background_task import *
from datetime import datetime

login_manager.init_app(app)
login_manager.login_view='login'
dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

@socketio.on('message from user',namespace='/chat')
@authenticated_only
def receive_message_from_user(message):
    print(request.sid)
    print('USER MESSAGE: {}'.format(message))
    emit('from flask', message.upper(),broadcast=True)

########################################################
#Chat
########################################################


@socketio.on('chat_message',namespace='/private_chat')
@authenticated_only
def handle_chat_message(msg):
    #print('Message:' + msg)
    chat_history = dynamodb.Table('CRM_chat_history')
    user = current_user.id
    time=datetime.now().time()
    send_messages(msg)
    update_message(msg)
    #start_background()

def update_message(msg):
    '''
    :param msg: SEND MESSAGE TO UPDATE IN REAL-TIME
    :return:
    '''
    timing = datetime.now().time()
    timing = str(timing)
    the_time = timing.split('.',1)[0]
    emit('chat_content_1', [msg,the_time])

def send_messages(msg):
    '''

    :param msg: Bringing in message to update the dynamodb
    :return:
    '''
    chat_history = dynamodb.Table('CRM_chat_history')
    try:
        response = chat_history.get_item(
            Key={
                'chat_id': 'leowyennhan@gmail.com_chat_dexterleow93@gmail.com',
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])

    else:
        item = response['Item']
        user1 = item['receiver_id']
        user2 = item['sender_id']
    if current_user.id == user1:
        recipient = user2
    else:
        recipient = user1
    session_table = dynamodb.Table('CRM-session')
    try:
        response = session_table.get_item(
            Key={
                'user_id': recipient,
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])

    else:
        timing = datetime.now().time()
        timing = str(timing)
        the_time = timing.split('.', 1)[0]
        try:
            item = response['Item']
            recipient_session_id = item['session_id']
            user = current_user.id
            chat_history.update_item(
                Key={
                    'chat_id': 'leowyennhan@gmail.com_chat_dexterleow93@gmail.com',

                },
                UpdateExpression="SET msg = list_append(msg, :r)",
                ExpressionAttributeValues={
                    ':r': [{'%s' % user: "%s" % msg, 'time': str(timing)}],
                },
                ReturnValues="UPDATED_NEW"
            )

            emit('chat_content_2', [msg,the_time], room=recipient_session_id)
        except Exception:
            user = current_user.id
            chat_history.update_item(
                Key={
                    'chat_id': 'leowyennhan@gmail.com_chat_dexterleow93@gmail.com',

                },
                UpdateExpression="SET msg = list_append(msg, :r)",
                ExpressionAttributeValues={
                    ':r': [{'%s' % user: "%s" % msg, 'time': str(timing)}],
                },
                ReturnValues="UPDATED_NEW"
            )




@socketio.on('connect')
def connected():
    the_session()
    pass

def the_session():
    session_table = dynamodb.Table('CRM-session')
    session_table.put_item(
        Item={
            'user_id': current_user.id,
            'session_id': request.sid
        })


'''
@socketio.on('username',namespace='/private')
def receive_username(username):
    #users.append({username:request.sid})
    users[username]=request.sid
    print('users name added')
    
@socketio.on('private_message',namespace='/private')
def private_message(payload):
    recipient_session_id=users[payload['username']]
    message=payload['message']
    emit('new_private_message',message, room=recipient_session_id)
'''
if __name__ == '__main__':
    socketio.run(app)