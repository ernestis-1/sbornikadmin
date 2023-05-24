import aiohttp
import asyncio

from aiohttp.helpers import content_disposition_header
from images_api import write_image, get_image_path_from_url

class BaseFacultyInfo:
    def __init__(self, fac_id=None, fac_name=None, abbreviation=None, fac_type=None, info=None, img_url=None, 
                phone_number=None, website_link=None, vk_link=None, instagram_link=None, facebook_link=None,
                sic_link=None, email=None, specialHashtagId = None):
        self.fac_id = fac_id
        self.fac_name = fac_name
        self.abbreviation = abbreviation
        self.fac_type = fac_type
        self.info = info
        self.img_url = img_url
        self.phone_number = phone_number
        self.website_link = website_link
        self.vk_link = vk_link
        self.instagram_link = instagram_link
        self.facebook_link = facebook_link
        self.sic_link = sic_link
        self.email = email
        self.specialHashtagId = specialHashtagId

    
    def init_from_dict(self, dict):
        self.fac_id = dict["id"]
        self.fac_name = dict["name"]
        self.abbreviation = dict["abbreviation"]
        self.fac_type = dict["type"]
        self.info = dict["info"]
        self.img_url = dict["picture"]
        self.phone_number = dict["phoneNumber"]
        self.website_link = dict["websiteLink"]
        self.vk_link = dict["vkLink"]
        self.instagram_link = dict["instagramLink"]
        self.facebook_link = dict["facebookLink"]
        self.sic_link = dict["sicLink"]
        self.email = dict["email"]
        #self.specialHashtagId = dict["specialHashtagId"]


class ContactInfo:
    def __init__(self, cont_id, cont_type, name, position, phone_number, links, photo_url, priority_number = -1):
        self.cont_id = cont_id
        self.cont_type = cont_type
        self.name = name
        self.position = position
        self.phone_number = phone_number
        self.links = links
        self.img_url = photo_url
        self.priority_number = priority_number


class FullFacultyInfo:
    def __init__(self, fac_id, fac_name, info, img_url, contacts):
        self.fac_id = fac_id
        self.fac_name = fac_name
        self.info = info
        self.img_url = img_url
        self.contacts = contacts


class FacultiesApi:
    def __init__(self, url_short, url_full=None, url_id=None, url_contact_types=None, url_faculties_types=None):
        self.url_short = url_short
        self.url_full = url_full
        self.url_id = url_id
        self.url_contact_types = url_contact_types
        self.url_faculties_types = url_faculties_types
    
    async def get_faculties(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url_short) as r:
                j = await r.json()
        l = []
        for fac in j:
            _id = fac["id"]
            _name = fac["name"]
            _abbreviation = fac["abbreviation"]
            _type = fac["type"]
            _info = fac["info"]
            _picture = fac["picture"]
            faculty_info = BaseFacultyInfo()
            faculty_info.init_from_dict(fac)
            l.append(faculty_info)
        return l

    async def get_faculty_info(self, fac_id, name):
        if fac_id:
            if self.url_id is None:
                return
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url_id+f"/{fac_id}") as r:
                    j = await r.json()
        elif name:
            json = {"name": name}
            async with aiohttp.ClientSession() as session:
                async with session.put(self.url_full, json=json) as r:
                    j = await r.json()
        else:
            return
        #_id = None 
        _id = j["id"]
        _name = j["name"]
        _info = j["info"]
        _picture = j["picture"]
        _contacts = j["contacts"]
        #print(_contacts)
        contacts = []
        for _contact in _contacts:
            contact = ContactInfo(_contact["id"], _contact["type"], _contact["name"], _contact["position"],
                    _contact["phoneNumber"], _contact["links"], _contact["photo"], priority_number=_contact["priorityNumber"])
            #print(contact.cont_type)
            contacts.append(contact)
        return contacts

    async def get_contacts_types(self, fac_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url_contact_types+f"/{fac_id}") as r:
                j = await r.json()
        return j

    async def get_faculties_types(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url_faculties_types) as r:
                j = await r.json()
        return j
