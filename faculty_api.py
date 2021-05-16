import aiohttp
import asyncio

from aiohttp.helpers import content_disposition_header
from sections_api import write_image, get_image_path_from_url

class BaseFacultyInfo:
    def __init__(self, fac_id, fac_name, info, img_url):
        self.fac_id = fac_id
        self.fac_name = fac_name
        self.info = info
        self.img_url = img_url


class ContactInfo:
    def __init__(self, cont_id, name, position, phone_number, links, photo_url):
        self.cont_id = cont_id
        self.name = name
        self.position = position
        self.phone_number = phone_number
        self.links = links
        self.img_url = photo_url


class FullFacultyInfo:
    def __init__(self, fac_id, fac_name, info, img_url, contacts):
        self.fac_id = fac_id
        self.fac_name = fac_name
        self.info = info
        self.img_url = img_url
        self.contacts = contacts


class FacultiesApi:
    def __init__(self, url_short, url_full=None, url_id=None):
        self.url_short = url_short
        self.url_full = url_full
        self.url_id = url_id
    
    async def get_faculties(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url_short) as r:
                j = await r.json()
        l = []
        for fac in j:
            _id = fac["id"]
            _name = fac["name"]
            _info = fac["info"]
            _picture = fac["picture"]
            l.append(BaseFacultyInfo(_id, _name, _info, _picture))
        return l

    async def get_faculty_info(self, fac_id, name):
        if name:
            json = {"name": name}
            async with aiohttp.ClientSession() as session:
                async with session.put(self.url_full, json=json) as r:
                    j = await r.json()
        elif fac_id:
            if self.url_id is None:
                return
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url_id+f"/{fac_id}") as r:
                    j = await r.json()
        else:
            return
        #_id = None 
        _id = j["id"]
        _name = j["name"]
        _info = j["info"]
        _picture = j["picture"]
        _contacts = j["contacts"]
        contacts = []
        for _contact in _contacts:
            contact = ContactInfo(_contact["id"], _contact["name"], _contact["position"],
                    _contact["phoneNumber"], _contact["links"], _contact["photo"])
            contacts.append(contact)
        return contacts

class GatherImages:
    def __init__(self, loop):
        self.images = []
        self.loop = loop

    async def add_image(self, session, local_id, image_url):
        filename = await get_image_path_from_url(session, image_url)
        self.images.append((local_id, filename))

    async def get_images(self, session, urls):
        tasks = []
        i = 0
        for url in urls:
            task = self.loop.create_task(self.add_image(session, i, url))
            tasks.append(task)
            i+=1
        await asyncio.gather(*tasks)
        paths = sorted(self.images, key=lambda pair: pair[0])
        return [path[1] for path in paths]
