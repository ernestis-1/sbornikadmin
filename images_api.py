import aiohttp, os, tempfile, asyncio, requests

# photo download

def write_image(data):
    _path = os.path.join(os.path.curdir, "tempfiles")
    if not os.path.exists(_path):
        os.mkdir(_path)
    if os.path.exists(_path):
        tmp_file = tempfile.NamedTemporaryFile(dir=_path)
        #print(tmp_file)
        tmp_name = tmp_file.name+".jpg"
        tmp_file.close()
        with open(tmp_name, "wb") as file:
            file.write(data)
        return tmp_name
    else:
        return None


def propper_session():
    return aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64,verify_ssl=False))

async def get_image_path_from_url(url, session=propper_session()):
    try:
        async with session.get(url) as response:
            data = await response.read()
            tmp_name = write_image(data)
            return tmp_name
    except Exception as err:
        print("Exception while getting picture\n"+str(err))
        return None

async def get_one_image(url):
    async with propper_session() as session:
        image_path = await get_image_path_from_url(url, session)
    return image_path

class GatherImages:
    def __init__(self, loop):
        self.images = []
        self.loop = loop

    async def add_image(self, local_id, image_url, session):
        if image_url != "" and image_url is not None:
            filename = await get_image_path_from_url(image_url, session)
        else:
            filename = None
        self.images.append((local_id, filename))

    async def get_many_images(self, urls):
        tasks = []
        i = 0
        async with propper_session() as session:
            for url in urls:
                task = self.loop.create_task(self.add_image(i, url, session))
                tasks.append(task)
                i+=1
            await asyncio.gather(*tasks)
        paths = sorted(self.images, key=lambda pair: pair[0])
        return [path[1] for path in paths]

# photo upload

def get_photo_uri(path_img):
    url = 'https://api.imgbb.com/1/upload?key=7739426e6cc4b2afe15d5db0e8272009'
    with open(path_img, 'rb') as img:
        name_img = os.path.basename(path_img)
        files = {'image': (name_img,img, 'multipart/form-data', {'Expires': '0'}) }
        with requests.Session() as s:
            r = s.post(url,files=files)
            #print(r.status_code)
            #print(r.text)
            json_response = r.json()
            #print(json_response)
            url_data = json_response['data']
            #print(f'Нужный url: {url_data["url"]}')
            return url_data["url"]