import os
import logging
import uuid
import socketio
import langid
from aiohttp import web
from rasa_sdk.executor import ActionExecutor
from rasa_sdk.interfaces import ActionExecutionRejection

import sys
sys.path.append('.')

from utils.bot_factory import BotFactory

langid.set_languages(['en', 'ms', 'zh'])

logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')


# Action executor config
executor = ActionExecutor()
executor.register_package('actions')

# Home page
async def index(request):
    index_file = open('./templates/index.html')
    return web.Response(body=index_file.read().encode('utf-8'), headers={'content-type': 'text/html'})


# Action endpoint
async def webhook(request):
    """Webhook to retrieve action calls."""
    action_call = await request.json()
    try:
        response = await executor.run(action_call)
    except ActionExecutionRejection as e:
        logger.error(str(e))
        response = {"error": str(e), "action_name": e.action_name}
        response.status_code = 400
        return response

    return web.json_response(response)


# Web app routing
app = web.Application()
app.add_routes([
    web.get('/', index),
    web.post('/webhook', webhook),
    web.static('/static', './static')
])

# Instantiate all bot agents
bots = BotFactory.createAll()

# Websocket through SocketIO with support for regular HTTP endpoints
sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
sio.attach(app)


@sio.on('session_request')
async def on_session_request(sid, data):
    if data is None:
        data = {}
    if 'session_id' not in data or data['session_id'] is None:
        data['session_id'] = uuid.uuid4().hex
    await sio.emit('session_confirm', data['session_id'])


@sio.on('user_uttered')
async def on_user_uttered(sid, message):
    custom_data = message.get('customData', {})
    # lang = custom_data.get('lang', 'en')
    user_message = message.get('message', '')
    lang, confidence = langid.classify(user_message)
    bot_responses = await bots[lang].handle_text(user_message)
    for bot_response in bot_responses:
        json = __parse_bot_response(bot_response)
        await sio.emit('bot_uttered', json, room=sid)


def __parse_bot_response(bot_response):
    # Images require a special schema
    if 'image' in bot_response:
        return { 'attachment': { 'type': 'image', 'payload': { 'src': bot_response['image'] }}}
    else:
        if 'buttons' in bot_response:
            # The JS client only shows the buttons when they arrive as 'quick_replies'
            bot_response['quick_replies'] = bot_response['buttons']
            del bot_response['buttons']

        # Remove the 'recipient_id', because the client can't handle it
        return {k: v for k, v in bot_response.items() if not k.startswith('recipient_id')}

def __create_env_js(host, port):
    f = None
    try:
        f = open("./static/js/env.js","w+")
        server_url=os.getenv('API_SERVER_URL', 'http://' + host + ':' + str(port))
        dict = {'serverUrl': server_url}
        f.write('Env=' + repr(dict))
    finally:
        if f is not None:
            f.close()

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8080))
    __create_env_js(host, port)
    web.run_app(app, host=host, port=port)
