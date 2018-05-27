from flask import *
from . import transacted
from flask_login import current_user,login_required
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import *
import boto3,requests,pprint

# login to AWS
session=boto3.Session()
credentials=session.get_credentials()
dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")

@transacted.route('/transactions',methods=['GET','POST'])
@login_required
def transactions():
    user = dynamodb.Table('CRM-user')
    response = user.get_item(
        Key={
            'user_id': current_user.id
        }
    )
    item = response['Item']
    name = item['name'][0]
    return render_template('transactions.html',name=name)

@transacted.route('/test',methods=['GET','POST'])
def card():
    return render_template('card-dashboard.html')