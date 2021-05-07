import requests
import tempfile
import os

class SectionInfo:
    def __init__(self, sect_id, name, img_url):
        self.sect_id = sect_id
        self.name = name
        self.img_url = img_url

    def get_image_path(self):
        try:
            p = requests.get(self.img_url)
        except Exception:
            return None
        _path = os.path.join(os.path.curdir, "tempfiles")
        if os.path.exists(_path):
            print("exists")
            out = open("img.jpg", "wb")
            out.write(p.content)
            out.close()
            tmp_file = tempfile.NamedTemporaryFile(dir=_path)
            tempname = tmp_file.name()
            tmp_file.close()
            os.rename(os.path.join(_path,"img.jpg"), tempname)


class SectionsApi:
    def __init__(self, url):
        self.url = url
    
    def get_sections(self):
        r = requests.get(self.url)
        j = r.json()
        l = []
        for sect in j:
            print(sect)
            _id = sect["id"]
            _name = sect["title"]
            _img_url = sect["picture"]
            print(_id)
            l.append(SectionInfo(_id, _name, _img_url))
        return l
