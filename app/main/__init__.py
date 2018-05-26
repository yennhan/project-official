from flask import Blueprint

main = Blueprint('main', __name__)
dash = Blueprint('dash', __name__)
mailbox = Blueprint('mail',__name__)
pro_company = Blueprint('pro_company',__name__)
transacted = Blueprint('transacted',__name__)
from . import routes, dashboard, event,mail_box,profile_company,transactions
