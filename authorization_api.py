import requests
import json
import global_constants
import aiohttp
import asyncio

class AuthorizationApi:
    def __init__(self, filename = "remember.json", remember_me=False, login=None, password=None):
        self.init_api(remember_me, login, password, filename)


    def init_api(self, remember_me=False, login=None, password=None, filename="remember.json"):
        if login:
            self.payload = {"login": login, "password": password}
            if remember_me:
                with open(filename,'w', encoding='utf8') as f:
                    json.dump(self.payload, f, ensure_ascii=False, indent=4)
        else:
            try:
                with open(filename) as f:
                    content = f.read()
                    if content:
                        self.payload = json.loads(content)
                    else:
                        self.payload = None
            except FileNotFoundError as fnfe:
                self.payload = None


    def get_token(self):
        #payload = {"login": self.login, "password": self.password}
        if self.payload:
            r = requests.post(global_constants.TOKEN_API, params=self.payload)
            if r.status_code == 200:
                j = r.json()
                token = j["access_token"]
                return token
            else:
                return None
        else:
            return None


class UserData:
    def __init__(self, login=None, password=None, role=None):
        self.login = login
        self.password = password
        self.role = role

    def init_from_dict(self, dict):
        self.login = dict["login"]
        if "password" in dict.keys():
            self.password = dict["password"]
        self.role = dict["role"]


class UserApi:
    def __init__(self, url=global_constants.USER_API, token=None):
        self.url = url
        self.token = token

    async def get_users(self):
        headers = {"Authorization": "Bearer "+self.token}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(self.url) as r:
                j = await r.json()
        l = []
        for user_dict in j:
            user_data = UserData()
            user_data.init_from_dict(user_dict)
            l.append(user_data)
        return l