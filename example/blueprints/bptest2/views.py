from flask import Blueprint

from example.app import socketio

from flask_socketio import emit, join_room, leave_room, \
    close_room, rooms, disconnect

bptest2 = Blueprint('bptest2', __name__)

@bptest2.route('/SendTallyFunc2/', methods=['GET','POST'])
def send_room_message_without_socketio():
        from example.blueprints.bptest2.tasks import test_tally_celery
        task = test_tally_celery.delay()
        print ('SENDING TO CELERY. Please wait..')
        return('Processing from BPTEST2.. please wait..')

@socketio.on('connect', namespace='/test_web2')
def test_connect():
    print('WEB CONNECTED ON OPEN AUTO')
    emit('web_response', {'data': 'Connected', 'count': 0})


@socketio.on('web_event', namespace='/test_web2')
def test_message(message):
    emit('web_response', {'data': message['data']})

@socketio.on('disconnect_request', namespace='/test_web2')
def local_disconnect_request():
    emit('lweb_response',
         {'data': 'Disconnected!'})
    socketio.sleep(0)
    print('WEB DISCONNECTED ON CLOSE/REFRESH')
    disconnect()