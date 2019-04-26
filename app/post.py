from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import aiohttp
from loguru import logger

from app import conf


@dataclass
class UploadItem:
    path: Path
    page_id: int
    name: str
    description: str
    upload_url = Optional[str]
    media_id = Optional[str]


class PostManager:
    def __init__(self):
        self.payload = {
            'v': conf.api_version,
            'access_token': conf.access_token
        }
        self.session = None

    async def init(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()

    async def post(self, url, data):
        logger.info(f'call {url}')
        result = await self.session.post(url, data=data)
        result_json = await result.json()
        return result_json

    async def pre_upload(self, item: UploadItem):
        url = 'https://api.vk.com/method/video.save'
        logger.info(f'Calling {url}')
        params = {
            **self.payload,
            'name': item.name,
            'group_id': item.page_id,
            'wallpost': 0,
        }
        logger.info(params)
        response = await self.post(url, data=params)
        logger.info(response)
        upload_url = response['response']['upload_url']
        item.upload_url = upload_url

    async def upload_video(self, item: UploadItem):
        logger.info(f'Uploading video. Calling {item.upload_url}')
        with open(item.path, 'rb') as video:
            response = await self.post(item.upload_url, data=video)
        item.media_id = response['video_id']

    async def post_to_wall(self, item: UploadItem):
        url = 'https://api.vk.com/method/wall.post'
        logger.info(f'Calling {url}')
        params = {
            **self.payload,
            'owner_id': f'-{item.page_id}',
            'from_group': 1,
            'message': item.description,
            'attachments': f'video-{item.page_id}_{item.media_id}'
        }
        response = await self.post(url, data=params)
        logger.info(response)
        return response

    async def upload_item(self, item: UploadItem):
        logger.info('Uploading item')
        await self.pre_upload(item)
        await self.upload_video(item)
        # TODO delay post_to_wall
        return await self.post_to_wall(item)
