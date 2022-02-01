import json
import os
import socket

from quart import Quart, render_template, send_from_directory, jsonify, abort

from app.utils.utilities import get_file_icon, convert_size


class SharedFiles:
    host = socket.gethostname()
    port = 80

    def __init__(self, mdapp):
        self.app = Quart(__name__)
        self.mdApp = mdapp
        self.files = []
        # ['C:\\Users\\banko\\Videos\\code breakers\\Code breaker E01 VOSTFR en DDL STREAMING.mp4', 'C:\\Users\\banko\\Videos\\code breakers\\Code breaker Episode 2 VOSTFR en DDL STREAMING.mp4', 'C:\\Users\\banko\\Videos\\code breakers\\Code breaker Episode 3 VOSTFR en DDL STREAMING.mp4', 'C:\\Users\\banko\\Videos\\code breakers\\Code breaker Episode 4 VOSTFR en DDL STREAMING.mp4', 'C:\\Users\\banko\\Videos\\code breakers\\Code breaker Episode 5 VOSTFR en DDL STREAMING.mp4', 'C:\\Users\\banko\\Videos\\code breakers\\Code breaker Episode 6 VOSTFR en DDL STREAMING.mp4', 'C:\\Users\\banko\\Videos\\code breakers\\Code breaker Episode 7 VOSTFR en DDL STREAMING.mp4', 'C:\\Users\\banko\\Videos\\code breakers\\Code breaker Episode 8 VOSTFR en DDL STREAMING.mp4', 'C:\\Users\\banko\\Videos\\code breakers\\Code breaker Episode 9 VOSTFR en DDL STREAMING.mp4', 'C:\\Users\\banko\\Videos\\code breakers\\Code breaker Episode 10 VOSTFR en DDL STREAMING.mp4', 'C:\\Users\\banko\\Videos\\code breakers\\Code breaker Episode 11 VOSTFR en DDL STREAMING.mp4', 'C:\\Users\\banko\\Videos\\code breakers\\Code breaker Episode 12 VOSTFR en DDL STREAMING.mp4', 'C:\\Users\\banko\\Videos\\code breakers\\Code breaker Episode 13 VOSTFR en DDL STREAMING.mp4']
        self.def_route()

    def def_route(self):
        @self.app.route('/')
        async def index():
            files = []
            pos = 0
            for file in self.files:
                if os.path.isfile(file[0]):
                    files.append((os.path.basename(file[0]), get_file_icon(file[0], type_only=True), "video" + str(pos),
                                  convert_size(os.path.getsize(file[0]))))
                    pos += 1
            # await flash('No image selected for uploading')
            return await render_template('index.html', files=files, data=json.dumps(files))

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
                if os.path.isfile(file[0]):
                    files.append(os.path.basename(file[0]))
            return jsonify(files)

        @self.app.route("/WebShare/files/<path:path>")
        async def get_file(path):
            for file in self.files:
                if os.path.basename(file[0]) == path:
                    return await send_from_directory(os.path.dirname(file[0]), path, as_attachment=True)
            abort(400, "No file allowed")

        @self.app.route("/WebShare/streamvideo/<path:path>")
        async def video_feed(path):
            for file in self.files:
                if os.path.basename(file[0]) == path:
                    return await send_from_directory(os.path.dirname(file[0]), path, conditional=True)
            abort(400, "No file allowed")

    def run(self):
        return self.app.run_task(host=self.host, port=self.port, debug=True)

    @staticmethod
    def get_url():
        return "http://" + SharedFiles.host + ":" + str(SharedFiles.port)
