# import asyncio
# import os
#
# from web.app import SharedFiles
#
# sha = SharedFiles("dsd")
# # shutil.copy(file, os.path.join(Path(__file__).resolve().parent, "static\\uploads"))
# # return redirect(url_for('static', filename='uploads/' + path), code=301)
# ft = os.path.getsize('C:\\Users\\banko\\Videos\\code breakers\\Code breaker E01 VOSTFR en DDL STREAMING.mp4')
# loop = asyncio.get_event_loop()
# loop.run_until_complete(sha.run())
# loop.close()
from app.utils.database_manager import DbManager

db = DbManager()
db.insertFiles([("path of first file", False), ("path of second file", False), ("path of third file", True)])

