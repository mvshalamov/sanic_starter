import asyncio
import ujson
from asyncpg import create_pool

import uvloop
from sanic import Sanic

from app.example import handlers
from app.settings import DATABASE_URL, DEBUG, MAX_NUM_DB_CONN, PORT, DATABASE_URL_READ

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

application = Sanic(__name__, log_config=None)


@application.listener('before_server_start')
async def register_db(app, loop): #pragma: no cover
    async def init(con):
        def _encoder(value):
            return b'\x01' + ujson.dumps(value).encode('utf-8')

        def _decoder(value):
            return ujson.loads(value[1:].decode('utf-8'))

        await con.set_type_codec(
            'jsonb', encoder=_encoder, decoder=_decoder, schema='pg_catalog', binary=True
        )

    app.pool = await create_pool(dsn=DATABASE_URL, loop=loop, max_size=MAX_NUM_DB_CONN, init=init)
    app.pool_read = await create_pool(dsn=DATABASE_URL_READ, loop=loop, max_size=MAX_NUM_DB_CONN, init=init)

application.add_route(handlers.ping, '/api/v1/ping', methods=['GET'])
application.add_route(handlers.THandler.as_view(), '/api/v1/thandler', methods=['GET', 'POST'])


def runserver(): #pragma: no cover
    application.run(host='0.0.0.0', port=PORT, debug=DEBUG, log_config=None)
