from json import JSONDecodeError
from aiohttp_apispec import docs, request_schema, setup_aiohttp_apispec

from aiohttp import web
from marshmallow import ValidationError

from message import send_message_to_all
from schemas import MessageSchema

routes = web.RouteTableDef()


@docs(
   tags=["telegram"],
   summary="Send message API",
   description="This end-point sends message to telegram bot user/users",
)
@routes.post("/")
async def index_get(request: web.Request) -> web.Response:
    try:
        payload = await request.json()
    except JSONDecodeError:
        return web.json_response({"result": "Request data is invalid"})

    try:
        schema = MessageSchema()
        data = schema.load(payload)
    except ValidationError as e:
        return web.json_response({"result": "Validation Error", "error": e.messages})

    await send_message_to_all(data.get("message"))
    return web.json_response({"result": "OK"})


if __name__ == "__main__":
    app = web.Application()
    setup_aiohttp_apispec(
        app=app, title="Hectar Bot documentation", version="v1.0",
        url="/api/docs/swagger.json", swagger_path="/api/docs",
    )

    app.add_routes(routes)
    web.run_app(app, port=5000)
