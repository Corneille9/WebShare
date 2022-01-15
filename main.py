from multiprocessing import Process

from app.dash import AppInstaller
from web.app import run_server

if __name__ == "__main__":
    AppInstaller().run()