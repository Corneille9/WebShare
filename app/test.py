import asyncio

from web.app import SharedFiles

sha = SharedFiles("dsd")

loop = asyncio.get_event_loop()
loop.run_until_complete(sha.run())
loop.close()