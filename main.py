import json

from aiohttp import web


FILENAME: str = "form.json"


def main() -> None:
    """Application entrypoint."""

    app = init_app()

    web.run_app(app)


async def get_async_application() -> web.Application:
    """Return async application instance."""

    app = await init_app()

    return app


async def init_app() -> web.Application:
    """
    Initiate application and setup it.

    :return: Application instance
    :rtype: web.Application
    """

    app = web.Application()

    setup_routes(app=app)

    return app


async def get_json_file(request: web.Request) -> web.Response:
    """
    Endpoint that returns json file content.

    :param request: Input data to endpoint
    :type request: web.Request
    :return: Json file content
    :rtype: web.Response
    """

    try:
        with open(FILENAME, "r") as file:
            data = json.loads(file.read())
    except FileNotFoundError:
        return web.Response(text="File doesn't exists, create it!")

    return web.json_response(text=json.dumps(data, indent=4))


async def set_json_file(request: web.Request) -> web.Response:
    """
    Endpoint that save json content to file.

    :param request: Input data to endpoint
    :type request: web.Request
    :return: Result of operation
    :rtype: web.Response
    """

    try:
        data = await request.json()
    except json.decoder.JSONDecodeError:
        return web.json_response(text=json.dumps({
            "error": "Incorrect json"
        }, indent=4))

    with open(FILENAME, "w") as file:
        file.write(json.dumps(data))

    return web.json_response(text=json.dumps({
        "successful": "Json saved to file"
    }, indent=4))


def setup_routes(*, app: web.Application) -> None:
    """
    Setup application routes.

    :param app: Current application
    :type app: web.Application
    """

    router = app.router
    router.add_get("/", get_json_file)
    router.add_post("/", set_json_file)


if __name__ == "__main__":
    main()
