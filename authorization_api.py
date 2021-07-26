import requests
import json
import global_constants

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