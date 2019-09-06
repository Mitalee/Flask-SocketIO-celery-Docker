
from . import bptest1
from example.app import create_celery_app, socketio

celery = create_celery_app()

@bptest1.route('/SendTallyFunc/', methods=['GET','POST'])
def send_room_message_without_socketio():
        from .tasks import test_tally_celery
        print('SENDING TO CELERY')
        tasks = test_tally_celery.delay()
        return ('Processing.. please wait..')


# @socketio.on('connect', namespace='/test_web2')
# def test_connect():
#     print('WEB CONNECTED ON OPEN AUTO')
#     emit('web_response', {'data': 'Connected', 'count': 0})


# @socketio.on('web_event', namespace='/test_web2')
# def test_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('web_response',
#          {'data': message['data'], 'count': session['receive_count']})

# @socketio.on('disconnect_request', namespace='/test_web2')
# def local_disconnect_request():
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     #print('in disconnect_request')
#     emit('web_response',
#          {'data': 'Disconnected!', 'count': session['receive_count']})
#     socketio.sleep(0)
#     print('WEB DISCONNECTED ON CLOSE/REFRESH')
#     disconnect()