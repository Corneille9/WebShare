import os
import socket

from quart import Quart, render_template, send_from_directory, jsonify, abort


class SharedFiles:
    def __init__(self, mdapp):
        self.app = Quart(__name__)
        self.mdApp = mdapp
        self.host = socket.gethostname()
        self.port = 80
        self.files = []
        self.route()

    def route(self):
        @self.app.route('/')
        async def index():
            files = []
            for file in self.files:
                if os.path.isfile(file):
                    files.append(os.path.basename(file))
            return await render_template('index.html', files=files)

        @self.app.route('/isConnected')
        async def isConnected():
            return 'true'

        @self.app.errorhandler(404)
        async def error_404(error):
            return await render_template("errors/404.html")

        @self.app.errorhandler(500)
        async def error_404(error):
            return await render_template("errors/500.html")

        @self.app.route("/WebShare/files")
        async def list_files():
            files = []
            for file in self.files:
                if os.path.isfile(file):
                    files.append(os.path.basename(file))
            return jsonify(files)

        @self.app.route("/WebShare/files/<path:path>")
        async def get_file(path):
            for file in self.files:
                if os.path.basename(file) == path:
                    return await send_from_directory(os.path.dirname(file), path, as_attachment=True)
            abort(400, "No file allowed")

    def run(self):
        return self.app.run_task(host=self.host, port=self.port, debug=True)
