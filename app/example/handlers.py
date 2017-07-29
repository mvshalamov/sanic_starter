from sanic.response import json

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from sanic.views import HTTPMethodView

from app.example.schemas import INSERT_TEST, GET_TEST
from app.example.sql import INSERT_SQL, GET_SQL


async def ping(request):
    """
    ping
    """
    res = {'answer': 'pong'}
    async with request.app.pool.acquire() as connection:
        sql = "SELECT 1;"
        await connection.execute(sql)
    return json(res)


class THandler(HTTPMethodView):
    async def get(self, request):
        print(request.args.items())
        input_args = {i: k[0] for i, k in request.args.items()}
        res = {'success': True}
        try:
            validate(input_args, GET_TEST)
        except ValidationError as e:
            res['success'] = False
            res['errors'] = [str(e)]
            return json(res, status=400)

        async with request.app.pool.acquire() as connection:
            result = await connection.fetch(
                GET_SQL
            )

        res['answer'] = result

        return json(res)

    async def post(self, request):
        res = {'success': True}

        input_args = request.json

        try:
            validate(input_args, INSERT_TEST)
        except ValidationError as e:
            res['success'] = False
            res['errors'] = [str(e)]
            return json(res, status=400)

        async with request.app.pool.acquire() as connection:
            id_res, = await connection.fetchrow(
                INSERT_SQL,
                input_args['name']
            )

        res['success'] = True
        res['answer'] = id_res

        return json(res)
