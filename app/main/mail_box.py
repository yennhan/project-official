from flask import redirect, url_for, render_template, request
from . import mailbox
import decimal
import boto3,json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, login_user,login_required,logout_user,current_user
from main1 import login_manager



dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

@mailbox.route("/mailbox")
@login_required
def mailbox():
    chat_history = dynamodb.Table('CRM_chat_history')
    user_online = dynamodb.Table('CRM-session')
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
        user = current_user.id
        user1 = item['receiver_id']
        user2 = item['sender_id']
        if current_user.id == user1:
            recipient = user2
        else:
            recipient = user1
    return render_template('mailbox.html', messages=item['msg'], username=user, second_user=recipient)