from flask import *
from . import transacted
from flask_login import current_user,login_required
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import *
import boto3,requests,pprint

# login to AWS
session=boto3.Session()
credentials=session.get_credentials()

@transacted.route('/transactions',methods=['GET','POST'])
def transactions():
    return render_template('transactions.html')