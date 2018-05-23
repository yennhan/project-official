from flask import *
from . import dash
from flask_login import current_user,login_required
import boto3
from boto3.dynamodb.types import TypeDeserializer
# login to AWS

dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")

@dash.route('/search',methods=['GET','POST'])
@login_required
def searching():
    if request.method == 'POST':
        search_item=request.form.get('searchbox')
        user_id = current_user.id
        print(search_item,user_id)
        return redirect(url_for('main.dashboard_login'))