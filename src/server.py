import aiohttp
import argparse
import jinja2
import toml

from aiohttp import web
import aiohttp_cors
import aiohttp_jinja2


@aiohttp_jinja2.template('index.html')
async def index(request):
    pass


async def get_api(request):
    language = request.match_info['language']
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://gitignore.io/api/{language}") as resp:
            resp_text = await resp.text()
            return web.Response(body=resp_text)


app = web.Application()
app['config'] = toml.load('config/settings.toml')
try:
    local_conf = toml.load('config/local.toml')
except FileNotFoundError as e:
    pass
else:
    app['config'].update(local_conf)


aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader('templates/'))


app.router.add_get('/', index)
app.router.add_get('/get-api/{language}', get_api)
if app['config']['debug']:
        app.router.add_static(
            '/static/', path='../static', name='static')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gitignoreyo')
    parser.add_argument('--port', default=8080)
    port = parser.parse_args().port
    web.run_app(app, host='0.0.0.0', port=int(port))
