import socket

from quart import Quart, render_template


class SharedFiles:
    def __init__(self, mdapp):
        self.app = Quart(__name__)
        self.mdApp = mdapp
        self.host = socket.gethostname()
        self.port = 80
        self.route()

    def route(self):
        @self.app.route('/')
        async def index():
            return await render_template('index.html')

        @self.app.route('/isConnected')
        async def isConnected():
            return 'true'

    def run(self):
        return self.app.run_task(host=self.host, port=self.port, debug=True)
