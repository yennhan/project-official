from flask import redirect, url_for, render_template, request
from . import main
import decimal
import boto3,json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, login_user,login_required,logout_user,current_user
from main1 import login_manager



dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
# Helper class to convert a DynamoDB item to JSON.

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

class User(UserMixin):
    user = dynamodb.Table('CRM-user')

    def __init__(self, user):
        self.id = user

    def __repr__(self):
        return "%d" % (self.id)

@login_manager.user_loader
def load_user(user):
    return User(user)

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = dynamodb.Table('CRM-user')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            response = user.get_item(
                Key={
                    'user_id': email
                }
            )
        except ClientError as e:
            return "%s" %(e.response['Error']['Message'])
        else:
            try:
               item = response['Item']
            except Exception:
                word="Invalid Username!  ..."
                return render_template('index.html',condition=word)
            else:
                if check_password_hash(item['password'],password):
                    user=User(email)
                    login_user(user)

                    return redirect(url_for('main.dashboard_login'))
                else:
                    word="Wrong Password"
                    return render_template('index.html',condition=word)


@main.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        company_id=request.form.get('company_id')
        first_name=request.form.get('firstname')
        last_name=request.form.get('lastname')
        email= request.form.get('email_address')
        phone_number=request.form.get('phone_number')
        company_name=request.form.get('company_name')
        company_address = request.form.get('company_address')
        company_type=request.form.get('company_type')
        employee_role=request.form.get('employee_role')
        company_industry=request.form.get('company_industry')
        password=request.form.get('password_a')
        hashed_password = generate_password_hash(password,method='sha256')
        multiselect = request.form.getlist('category_tags_value')
        list = {}
        list['company_name'] = company_name
        list['company_address'] = company_address
        list['company_type']=company_type
        list['company_tags']=multiselect
        user = dynamodb.Table('CRM-user')
        user.put_item(
            Item={
                'user_id': email,
                'password': hashed_password,
                'name':[first_name,last_name],
                'phone_no':phone_number,
                'employee_role':employee_role,
                'company_id': company_id,
                'company_industry':company_industry,
                'company_details':list

            })
    return redirect(url_for('main.index'))

'''
        video_id="company2"
        response = user.query(
            IndexName='company_id',
            KeyConditionExpression=Key('company_id').eq(video_id)
        )
'''
@main.route('/dashboard_login',methods=['GET','POST'])
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



@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@main.route("/logout")
@login_required
def logout():
    session_table = dynamodb.Table('CRM-session')
    session_table.delete_item(
        Key={
            'user_id': current_user.id,
        })
    logout_user()
    print('You have been logged out.')
    return redirect(url_for('main.index'))


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
        word = 'leowyennhan@gmail.com_chat_dexterleow93@gmail.com'
        u = word.split('_chat_')
        print(u[0], u[1])
        user = u[0]
    return render_template('mailbox.html',messages=item['msg'],username=user,second_user=u[1])

 chat_history.update_item(
        Key={
            'chat_id': 'leowyennhan@gmail.com_chat_dexterleow93@gmail.com',

        },
        UpdateExpression="SET msg = list_append(msg, :r)",
        ExpressionAttributeValues={
            ':r': [{'%s' % "leowyennhan@gmail.com": "hello world2"}],
        },
        ReturnValues="UPDATED_NEW"
    )
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
        print("GetItem succeeded:")
        for i in item['msg']:
            print(i['leowyennhan@gmail.com'])
        word='leowyennhan@gmail.com_chat_dexterleow93@gmail.com'
        test=word.split('_chat_')
        print(test[0],test[1])
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
        print("GetItem succeeded:")
        for i in item['msg']:
            print(i)
    '''