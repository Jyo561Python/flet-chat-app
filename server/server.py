import socketio

sio = socketio.AsyncServer(async_mode='asgi')

app = socketio.ASGIApp(sio)

@sio.on('connection')
async def connect(event, sid, data):
	print(f'user {sid} is connected')

@sio.on('message')
async def messag(event, mydata):
	await emit('message:received', {'data': mydata}, broadcast=True, include_self=False)

@sio.on('disconnect')
async def discon(event, sid, mydata):
	print(f'user {sid} left.')
