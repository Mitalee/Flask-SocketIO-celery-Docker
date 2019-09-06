#!/usr/bin/env python
import eventlet
eventlet.monkey_patch(socket=True)
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

from celery import Celery

#from example.blueprints.bptest2 import bptest2
#from example.blueprints.bptest2 import tasks

socketio = SocketIO()


CELERY_TASK_LIST = [
    'example.blueprints.bptest1.tasks',
    'example.blueprints.bptest2.tasks',
]


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker='redis://:devpassword@redis:6379/0',
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app(main=True, debug=False):
    """Create an application."""
    app = Flask(__name__)
    #app.config.from_object(config[config_name])
    #config[config_name].init_app(app)
    #app.debug = debug

    async_mode = None

    app.config['SECRET_KEY'] = 'secret!'

    # for socketio
    #socketio = SocketIO(app, logger=True, engineio_logger=True, message_queue=app.config['CELERY_BROKER_URL'])

    #socketio = SocketIO()
    #   socketio = SocketIO(None, logger=True, engineio_logger=True, message_queue=app.config['CELERY_BROKER_URL'], async_mode='threading')
    # # Initialize Celery

    from example.blueprints.bptest2 import bptest2
    app.register_blueprint(bptest2)

    from example.blueprints.bptest1 import bptest1
    app.register_blueprint(bptest1)

    #socketio.init_app(app, logger=True, engineio_logger=True, async_mode=async_mode, message_queue='redis://:devpassword@redis:6379/0')

    #######PUT THIS AFTER REGISTERING THE BLUEPRINT
    if main:
        # Initialize socketio server and attach it to the message queue, so
        # that everything works even when there are multiple servers or
        # additional processes such as Celery workers wanting to access
        # Socket.IO
        socketio.init_app(app, logger=True, engineio_logger=True, 
                          message_queue='redis://:devpassword@redis:6379/0')
        #socketio = SocketIO(app, logger=True, engineio_logger=True, message_queue=app.config['CELERY_BROKER_URL'])
    else:
        # Initialize socketio to emit events through through the message queue
        # Note that since Celery does not use eventlet, we have to be explicit
        # in setting the async mode to not use it.
        socketio.init_app(None, logger=True, engineio_logger=True, 
                          message_queue='redis://:devpassword@redis:6379/0',
                          async_mode='threading')

    @app.route('/')
    def index():
        return render_template('index.html', async_mode=socketio.async_mode)


    return app