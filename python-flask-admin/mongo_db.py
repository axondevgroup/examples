# Third party import
import pymongo

# Local application imports
from flask import (
    _app_ctx_stack,
    current_app
)


class MongoConnector(object):
    """Pymongo.MongoClient wrapper

       Wraps default MongoClient for proper database
       working with flask app context. Also handles
       connection with MongoDB and close it while app
       exited
    """
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    def connect(self):
        db_host = current_app.config.get('DB_HOST', None)
        db_port = int(current_app.config.get('DB_PORT', None))
        db_username = current_app.config.get('DB_USERNAME', None)
        if db_username is not None:
            db_password = current_app.config.get('DB_PASSWORD', None)
            db_auth_src = current_app.config.get('DB_NAME', None)
            mongo_client = pymongo.MongoClient(host=db_host,
                                               port=db_port,
                                               username=db_username,
                                               password=db_password,
                                               authSource=db_auth_src)
        else:
            mongo_client = pymongo.MongoClient(host=db_host,
                                               port=db_port)
        
        return mongo_client


    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'mongo_db'):
            ctx.mongo_db.close()

    @property
    def connection(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'mongo_db'):
                ctx.mongo_db = self.connect()
            return ctx.mongo_db

    @property
    def get_db(self):
        return self.connection[current_app.config.get('DB_NAME', None)]
