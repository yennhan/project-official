from flask import *
from . import dash
from flask_login import current_user,login_required
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import *
import boto3,requests

# login to AWS
session=boto3.Session()
credentials=session.get_credentials()

auth=AWS4Auth(credentials.access_key ,credentials.secret_key,'ap-southeast-1','es')
dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
client_es = boto3.client('es',endpoint_url= "https://search-inventory-5ucv2n3ftxe7aqer4hh7gi7pha.ap-southeast-1.es.amazonaws.com/")
link="https://search-inventory-5ucv2n3ftxe7aqer4hh7gi7pha.ap-southeast-1.es.amazonaws.com/crm-company/"
host="https://search-inventory-5ucv2n3ftxe7aqer4hh7gi7pha.ap-southeast-1.es.amazonaws.com"
#client=Elasticsearch([host])
#response = requests.get(host, auth=auth)


#print("Got %d Hits:" % data['hits']['total'])
#for hit in data['hits']['hits']:
    #print( hit["_source"])

#print(the_word)
es=Elasticsearch(hosts=[{'host': "search-inventory-5ucv2n3ftxe7aqer4hh7gi7pha.ap-southeast-1.es.amazonaws.com",'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
            )
#res = es.search(index="crm-company", body={"query": {"match_all": {}}})


@dash.route('/dashboard_login',methods=['GET','POST'])
@login_required
def dashboard_login():
    user = dynamodb.Table('CRM-user')
    response = user.get_item(
        Key={
            'user_id': current_user.id
        }
    )
    item = response['Item']
    name=item['name'][0]
    return render_template('dashboard.html',name=name,username=name)

@dash.route('/dash_result',methods=['GET','POST'])
@login_required
def dash_one():
    user = dynamodb.Table('CRM-user')
    response = user.get_item(
        Key={
            'user_id': current_user.id
        }
    )
    item = response['Item']
    name = item['name'][0]
    key2 = request.args.get('no_res')
    if key2=="empty":
        print(key2)
    else:
        keys = request.args.get('resulting')
        print(keys)

    return render_template('dashboard.html', name=name, username=name)
@dash.route('/search',methods=['GET','POST'])
@login_required
def searching():
    if request.method == 'POST':
        search_item=request.form.get('searchbox')
        user_id = current_user.id
        #print(search_item)
        query = es.search(index="crm-company", q=search_item)
        #print("Got %d Hits:" % query['hits']['total'])
        #for hit in query['hits']['hits']:
            #print( hit["_source"])
        if (query['hits']['total']==0):
            the_result = "empty"
        else:
            the_result="not_empty"
        the_hit_result=query["hits"]["hits"]
        return redirect(url_for('dash.dash_one',resulting=[the_hit_result],no_res=the_result))