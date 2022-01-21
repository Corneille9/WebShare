import os
import socket

from quart import Quart, render_template, send_from_directory, jsonify, abort

from app.utils.utilities import get_file_icon


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
            pos = 0
            for file in self.files:
                if os.path.isfile(file):
                    files.append((os.path.basename(file), get_file_icon(file, type_only=True), pos, "200MB"))
                    pos += 1
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

        @self.app.route("/WebShare/video_feed/<path:path>")
        async def video_feed(path):
            for file in self.files:
                if os.path.basename(file) == path:
                    
                    pass
            abort(400, "No file allowed")

    def run(self):
        return self.app.run_task(host=self.host, port=self.port, debug=True)
