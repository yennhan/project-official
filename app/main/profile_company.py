from flask import redirect, url_for, render_template, request
from . import pro_company
import boto3
from flask_login import current_user,login_required


dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")


@pro_company.route('/company_profile',methods=['GET','POST'])
@login_required
def profile_homepage():
    user = dynamodb.Table('CRM-user')
    response = user.get_item(
        Key={
            'user_id': current_user.id
        }
    )
    item_1 = response['Item']
    company = dynamodb.Table('CRM-company')
    response = company.get_item(
        Key={
            'company_id': item_1['company_id']
        }
    )
    item = response['Item']
    return render_template('page-profile.html',the_list=item,the_settings="")

@pro_company.route('/load_profile',methods=['GET','POST'])
@login_required
def profile_company():
    id=request.form.get('company_id')
    company = dynamodb.Table('CRM-company')
    response = company.get_item(
        Key={
            'company_id': id
        }
    )
    item = response['Item']
    return render_template('page-profile.html',the_list=item,the_settings="display:none")