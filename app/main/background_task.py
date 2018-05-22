#!/bin/env python

from main1 import socketio

'''
def start_session():
    global thread
    thread = socketio.start_background_task(target=session_key)

def session_key():
    count = 0
    while True:
        socketio.sleep(5)
        count += 1
        print("update" + str(count))
        if count == 10:
            break
'''
def start_background():
    global thread
    thread = socketio.start_background_task(target=update_chat)
    thread = socketio.start_background_task(target=get_Chat)

def update_chat():
    count = 0
    while True:
        socketio.sleep(5)
        count += 1
        print("update" + str(count))
        if count==10:
            break

def get_Chat():
    count = 0
    while True:
        socketio.sleep(1)
        count += 1
        print("Pewpewpew" + str(count))
