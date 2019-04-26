import logging
import sys
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel

from app import conf
from app.model import Channel, database
from app.post import PostManager, UploadItem


def init_logging():
    config = {
        'handlers': [
            {
                'sink': Path(conf.root_dir) / conf.log_file,
                'level': 'DEBUG',
                'rotation': '1 week'
            },
        ],
    }
    if conf.stdout_log:
        config['handlers'].append({'sink': sys.stdout, 'level': 'DEBUG'})
    logger.configure(**config)

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            logger_opt = logger.opt(depth=6, exception=record.exc_info)
            logger_opt.log(record.levelname, record.getMessage())

    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().addHandler(InterceptHandler())


init_logging()
manager = PostManager()
app = FastAPI()


class Video(BaseModel):
    cam: str
    path: str
    name: str
    description: str


class ChannelBase(BaseModel):
    cam: str = None
    group_id: int = None


class ChannelCreate(ChannelBase):
    cam: str
    group_id: int


class ChannelInDBBase(ChannelBase):
    id: int
    cam: str
    group_id: int


class ChannelDB(ChannelInDBBase):
    pass


@app.on_event('startup')
async def startup_event():
    await database.connect()
    await manager.init()


@app.on_event('shutdown')
async def startup_event():
    await manager.stop()
    await database.disconnect()


@app.post('/upload_item')
async def upload_item(item: Video):
    logger.info('uploading item..')
    channel = await Channel.objects.filter(cam=item.cam).all()
    if len(channel) < 1:
        raise HTTPException(status_code=404, detail='Cam not found')
    if len(channel) > 1:
        raise HTTPException(status_code=409, detail='There are several channels with same cam name')
    channel = channel[0]
    item = UploadItem(Path(item.path), channel.group_id, item.name, item.description)
    try:
        response = await manager.upload_item(item)
    except Exception:
        logger.exception('Unhandled error during item posting')
        response = 'Error'
    return response


@app.get('/channels', response_model=List[ChannelDB])
async def list_channels():
    items = await Channel.objects.all()
    return items


@app.post('/add_channel', response_model=ChannelDB)
async def add_channel(channel: ChannelCreate):
    channel = await Channel.objects.create(cam=channel.cam, group_id=channel.group_id)
    return channel
