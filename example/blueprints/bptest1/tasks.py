
# from . import bptest1

from flask_socketio import SocketIO

from .views import celery
#from example.app import socketio


@celery.task(bind=True)
def test_tally_celery(self):
	print('IN CELERY BACKGROUND TASK')
	sio = SocketIO(logger=True, engineio_logger=True, message_queue='redis://:devpassword@redis:6379/0', async_mode='threading')
	#from example.app import socketio as sio
	message = None
	self.update_state(state='PROGRESS',
                          meta={'current': 'working'})
	#sio.emit('local_request',{'data': message }, namespace='/test_local', broadcast=True)
	#sio.sleep(1)
	sio.emit('web_response1', {'data': 'SENT MESSAGE THROUGH CELERY BPTEST1'}, broadcast=True, namespace='/test_web2')
	sio.sleep(1)
	print('TRIED EMIT FROM CELERY BPTEST1')
	return('tried to print')
