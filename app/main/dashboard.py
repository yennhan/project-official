from flask import *
from . import dash

from flask_login import current_user,login_required
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import *
import boto3,uuid,requests,pprint

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
    return render_template('dashboard.html',list_of_search=None,name=name,username=name)

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
    the_company = item['company_id']
    search_item=request.args.get('q')
    query = es.search(index="crm-company", q=search_item)
    #for hit in query['hits']['hits']:
        #pprint.pprint(hit['_source'])
    if (query['hits']['total']==0):
        return render_template('dashboard.html',list_of_search=None, name=name, username=name)
    else:
        return render_template('dashboard.html', list_of_search=query, name=name, username=name,comp_id=the_company)


@dash.route('/search',methods=['GET','POST'])
@login_required
def searching():
    if request.method == 'POST':
        search_item=request.form.get('searchbox')
        #print("Got %d Hits:" % query['hits']['total'])
        return redirect(url_for('dash.dash_one',q=search_item))

@dash.route('/submit_enquiry',methods=['GET','POST'])
@login_required
def submit_enquiry():
    print (request.form)
    if request.method == 'POST':
        id = request.form['company_id_1']
        comments = request.form['comment']
        try:
            file = request.files['config_file']
        except Exception:
            print(id,comments)
            pass
        else:
            print("There is a file"+str(file))
        user = dynamodb.Table('CRM-user')
        response = user.get_item(
            Key={
                'user_id': current_user.id
            }
        )
        item = response['Item']
        the_company=item['company_id']
        comp = dynamodb.Table('CRM-company')
        the_resp = comp.get_item(
            Key={
                'company_id': the_company
            }
        )
        the_p = the_resp['Item']
        comp_name=the_p['company_name']
        docs_table=dynamodb.Table('CRM-Docs')
        docs_table.put_item(
            Item={
                'doc_id': str(uuid.uuid4()),
                'company_id': id,
                'sender_company_id': the_company,
                'company_name':comp_name,
                'comments':comments,
                'requirements':"Initiate For Bidding "
            }
        )

        return render_template('page-profile.html', the_list=item, the_settings="display:none")
