import math
from pathlib import Path


def get_file_icon(path, type_only=False):
    pos = path[::-1].find(".")
    if pos != -1:
        extension = path[-path[::-1].find("."):]
        if extension_box.get("images").__contains__(extension):
            if type_only:
                return "images"
            return icon_dict.get("images")
        elif extension_box.get("videos").__contains__(extension):
            if type_only:
                return "videos"
            return icon_dict.get("videos")
        elif extension_box.get("musics").__contains__(extension):
            if type_only:
                return "musics"
            return icon_dict.get("musics")
        elif extension_box.get("document").__contains__(extension):
            if type_only:
                return "document"
            return icon_dict.get("document")
        elif extension_box.get("word").__contains__(extension):
            if type_only:
                return "word"
            return icon_dict.get("word")
        elif extension_box.get("powerPoint").__contains__(extension):
            if type_only:
                return "powerPoint"
            return icon_dict.get("powerPoint")
        elif extension_box.get("archive").__contains__(extension):
            if type_only:
                return "archive"
            return icon_dict.get("archive")

    return icon_dict.get("unknown")


def get_icon_dir():
    return str(Path(__file__).resolve().parent.parent) + "\\res\\icon\\"


def convert_size(size):
    if size == 0:
        return '0B'
    size_types = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)
    return "%s%s" % (s, size_types[i])


extension_box = {
    "images": ["png", "jpg", "jpeg", "gif", "bmp", "webp", "ico"],
    "videos": ["mp4", "mov", "mkv", "avi", "webm"],
    "musics": ["mp3"],
    "pdf": ["pdf"],
    "document": ["txt", "py", "data", "java", "css", "html", "csv", "json"],
    "word": ["docx"],
    "powerPoint": ["pptx"],
    "archive": ["zip", "7z"]
}

icon_dict = {
    "images": "Image.png",
    "videos": "Video.png",
    "musics": "Music.png",
    "pdf": "Unknown.png",
    "document": "Document.png",
    "word": "Word.png",
    "powerPoint": "PowerPoint.png",
    "unknown": "Unknown.png",
    "archive": "Zip.png",
}
