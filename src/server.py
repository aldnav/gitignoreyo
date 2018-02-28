import argparse
import jinja2
import toml

from aiohttp import web
import aiohttp_cors
import aiohttp_jinja2


@aiohttp_jinja2.template('index.html')
async def index(request):
    pass


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
if app['config']['debug']:
        app.router.add_static(
            '/static/', path='../static', name='static')

cors = aiohttp_cors.setup(app, defaults={
    '*': aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers='*',
        allow_headers='*')
})

print(cors)
for route in list(app.router.routes()):
    cors.add(route)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gitignoreyo')
    parser.add_argument('--port', default=8080)
    port = parser.parse_args().port
    web.run_app(app, host='0.0.0.0', port=int(port))
