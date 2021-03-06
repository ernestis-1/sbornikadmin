from email.mime import image
import aiohttp
import images_api
import asyncio


class SectionInfo:
    def __init__(self, sect_id, name, img_url):
        self.sect_id = sect_id
        self.name = name
        self.img_url = img_url

    async def get_image_path(self):
        return await images_api.get_image_path_from_url(self.img_url)


class ArticleInfo:
    def __init__(self, article_id, article_title):
        self.article_id = article_id
        self.article_title = article_title


class SectionsApi:
    def __init__(self, url):
        self.url = url
    
    async def get_sections(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as r:
                j = await r.json()
        #r = requests.get(self.url)
        #j = r.json()
        l = []
        for sect in j:
            #print(sect)
            _id = sect["id"]
            _name = sect["title"]
            _img_url = sect["picture"]
            #print(_id)
            l.append(SectionInfo(_id, _name, _img_url))
        return l

    async def get_articles(self, sect_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url+f"/{sect_id}") as r:
                j = await r.json()
        l = []
        try:
            data = j['data']
        except Exception as e:
            return None
        if j['type'] == "article":
            l.append(ArticleInfo(data['id'], data['title']))
            return l
        for article_data in data:
            l.append(ArticleInfo(article_data['id'], article_data['title']))
        return l
        

class FullArticleInfo:
    def __init__(self, article_id, article_title, article_text, parent_id, pictures_urls):
        self.article_id = article_id
        self.article_title = article_title
        self.article_text = article_text
        self.parent_id = parent_id
        self.pictures_urls = pictures_urls

    async def get_images(self):
        filenames = []
        loop = asyncio.get_event_loop()
        gather = images_api.GatherImages(loop)
        filenames = await gather.get_many_images(self.pictures_urls)
        filenames = [fname for fname in filenames if fname]
        # for url in self.pictures_urls:
        #     filename = await get_image_path_from_url(session, url)
        #     if filename:
        #         filenames.append(filename)
        return filenames


class ArticleApi:
    def __init__(self, url):
        self.url = url

    async def get_article(self, article_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url+f"/{article_id}") as r:
                j = await r.json()
        return FullArticleInfo(article_id=j['id'], article_title=j['title'], article_text=j['text'], parent_id=j['parentId'], pictures_urls=j['pictures'])