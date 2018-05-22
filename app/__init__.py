from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO


socketio = SocketIO(manage_sesison=False,async_mode='eventlet')
login_manager = LoginManager()

def create_app(debug=False):
    """Create an application."""
    import eventlet
    eventlet.monkey_patch()
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    from .main import main as main_blueprint
    from .main import dash as dash_blueprint
    from .main import mailbox as mail_blueprint
    from .main import pro_company as co_prof_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(dash_blueprint)
    app.register_blueprint(mail_blueprint)
    app.register_blueprint(co_prof_blueprint)
    socketio.init_app(app)
    return app