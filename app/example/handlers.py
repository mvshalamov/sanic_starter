from sanic.response import json

from app.example.schemas import POST_TEST, GET_TEST
from app.example.sql import INSERT_SQL, GET_SQL
from utils import JsonSchemaHTTPMethodView, ApiError, get_result_dict


async def ping(request):
    """
    ping
    """
    async with request.app.pool.acquire() as connection:
        sql = "SELECT 1;"
        await connection.execute(sql)
    return json(get_result_dict('pong'))


class THandler(JsonSchemaHTTPMethodView):
    _schemas = {
        'GET': GET_TEST,
        'POST': POST_TEST
    }

    async def get(self, request):
        async with request.app.pool.acquire() as connection:
            result = await connection.fetch(
                GET_SQL
            )

        return json(get_result_dict(result))

    async def post(self, request):
        async with request.app.pool.acquire() as connection:
            id_res, = await connection.fetchrow(
                INSERT_SQL,
                # JSON request body after validation is stored in self._data
                self._data['name']
            )

        return json(get_result_dict(id_res))

    async def put(self, request):
        raise ApiError(['Test API error'], 400)
