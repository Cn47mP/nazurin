from aiogram.dispatcher import filters
from aiogram.types import Message

from nazurin import bot
from nazurin.utils import NazurinError, sendDocuments, sendPhotos

from .api import Danbooru

danbooru = Danbooru()

@bot.handler(filters.RegexpCommandsFilter(regexp_commands=[r'/danbooru (\S+)'])
             )
async def danbooru_view(message: Message, regexp_command):
    try:
        post_id = int(regexp_command.group(1))
        if post_id <= 0:
            await message.reply('Invalid post id!')
            return
        imgs, details = danbooru.view(post_id)
        await sendPhotos(message, imgs, details)
    except (IndexError, ValueError):
        await message.reply('Usage: /danbooru <post_id>')
    except NazurinError as error:
        await message.reply(error.msg)
    # except BadRequest as error:
    #     handleBadRequest(message, error)

@bot.handler(
    filters.RegexpCommandsFilter(regexp_commands=[r'/danbooru_download (\S+)'])
)
async def danbooru_download(message: Message, regexp_command):
    try:
        post_id = int(regexp_command.group(1))
        if post_id <= 0:
            await message.reply('Invalid post id!')
            return
        imgs = await danbooru.download(post_id)
        await sendDocuments(message, imgs)
    except (IndexError, ValueError):
        await message.reply('Usage: /danbooru_download <post_id>')
    except NazurinError as error:
        await message.reply(error.msg)

commands = [danbooru_view, danbooru_download]
