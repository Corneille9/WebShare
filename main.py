import asyncio

from app.dash import AppInstaller

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(AppInstaller().app_func())
    loop.close()
