import os

from app.dash import AppInstaller
from web.api_design.api_design.settings import BASE_DIR

if __name__ == "__main__":
    AppInstaller().run()
    # print(os.system(os.path.join(BASE_DIR, "manage.py runserver 192.168.43.214:80")))
