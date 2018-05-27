from flask import *
from . import transacted
from flask_login import current_user,login_required
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import *
from boto3.dynamodb.conditions import Key
import boto3,requests,pprint,uuid

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
    company=item['company_id']
    name = item['name'][0]
    docs_table = dynamodb.Table('CRM-Docs')
    response = docs_table.query(
        IndexName='company_id-index',
        KeyConditionExpression=Key('company_id').eq(company)
    )
    the_result=response['Items']
    print(the_result)
    return render_template('transactions.html',name=name,the_list=the_result)


@transacted.route('/test',methods=['GET','POST'])
def card():
    return render_template('card-dashboard.html')