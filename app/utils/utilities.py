def get_file_icon(path):
    pos = path[::-1].find(".")
    if pos != -1:
        extension = path[-path[::-1].find("."):]
        if extension_box.get("images").__contains__(extension):
            return icon_dict.get("images")
        elif extension_box.get("videos").__contains__(extension):
            return icon_dict.get("videos")
        elif extension_box.get("musics").__contains__(extension):
            return icon_dict.get("musics")
        elif extension_box.get("document").__contains__(extension):
            return icon_dict.get("document")
        elif extension_box.get("word").__contains__(extension):
            return icon_dict.get("word")
        elif extension_box.get("powerPoint").__contains__(extension):
            return icon_dict.get("powerPoint")
        elif extension_box.get("archive").__contains__(extension):
            return icon_dict.get("archive")

    return icon_dict.get("unknown")


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
    "images": "app/res/icon/Image.png",
    "videos": "app/res/icon/Video.png",
    "musics": "app/res/icon/Music.png",
    "pdf": "app/res/icon/Unknown.png",
    "document": "app/res/icon/Document.png",
    "word": "app/res/icon/Word.png",
    "powerPoint": "app/res/icon/PowerPoint.png",
    "unknown": "app/res/icon/Unknown.png",
    "archive": "app/res/icon/Zip.png",
}
