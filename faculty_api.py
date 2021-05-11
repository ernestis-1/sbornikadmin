import aiohttp

class BaseFacultyInfo:
    def __init__(self, fac_id, fac_name, info):
        self.fac_id = fac_id
        self.fac_name = fac_name
        self.info = info




class FacultiesApi:
    def __init__(self, url_short, url_full=None):
        self.url_short = url_short
        self.url_full = url_full
    
    async def get_faculties(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url_short) as r:
                j = await r.json()
        l = []
        for fac in j:
            _id = fac["id"]
            _name = fac["name"]
            _info = fac["info"]
            l.append(BaseFacultyInfo(_id, _name, _info))
        return l
