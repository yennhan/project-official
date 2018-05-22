from flask_socketio import send,emit
from flask import session
from .. import socketio

from flask_login import UserMixin, login_user,login_required,logout_user,current_user

#'user_id'= current_user.id

@socketio.on('message')
def handleMessage(msg):
    print('Messageo'+msg)
    emit(msg, broadcast=True)


@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})
