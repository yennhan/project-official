from flask import redirect, url_for, render_template, request
from . import pro_company
import boto3
from flask_login import current_user,login_required


dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")


@pro_company.route('/company_profile',methods=['GET','POST'])
@login_required
def profile_homepage():
    return render_template('page-profile.html')