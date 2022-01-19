import asyncio

from app.dash import WebShare

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(WebShare().app_func())
    loop.close()
