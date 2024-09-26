import asyncio
import logging
import sys
from config import *

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command 
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, BotCommand
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils import init_db
from models import User, Post, Link
from config import NOTIFY_GROUP
import re

def validate_url(url):
    # Регулярное выражение для валидации ссылок
    pattern = re.compile(r'^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/[\w\-./?%&=]*)?$')
    
    # Проверка соответствия
    return bool(pattern.match(url))


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = await User.get_or_create(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        language_code=message.from_user.language_code
    )
    
    commands = [
        BotCommand(
            command='start',
            description='Перезапусти бота'
        ),
        BotCommand(
            command='add',
            description='Добавить ссылку'
        )
    ]

    await message.bot.set_my_commands(commands=commands)
    
    welcome_post = await Post.get(tag='welcome')
    await message.answer_video_note(
        video_note=welcome_post.video_note_id,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Продолжить', callback_data='continue')]])
    )


@dp.callback_query(F.data == "continue") 
async def callback_continue_handler(query: CallbackQuery):
    main_post = await Post.get(tag='main')
    await query.message.answer(main_post.text, disable_web_page_preview=True)


class Form(StatesGroup):
    link = State()


@dp.message(Command('add'))
async def command_add_handler(message: Message, state: FSMContext) -> None:
    add_link = await Post.get(tag='add_link')
    await state.set_state(Form.link)
    await message.answer(
        add_link.text,
    )
    

@dp.message(Form.link)
async def process_link(message: Message, state: FSMContext) -> None:
    user = await User.get(user_id=message.from_user.id)
    # Validate message.text to url
    if not validate_url(message.text):
        fail_link_post = await Post.get(tag='fail_link')
        await message.answer(
            fail_link_post.text,
        )
        return
    
    if len(await Link.filter(url=message.text)) > 0:
        link_exists_post = await Post.get(tag='link_exists')
        await message.answer(
            link_exists_post.text,
        )
        return
    
    correct_link_post = await Post.get(tag='correct_link')
    await message.answer(
        correct_link_post.text, 
    )
    await Link.create(
        user=await User.get(user_id=message.from_user.id),
        url=message.text    
    )
    
    await message.bot.send_message(
        chat_id=NOTIFY_GROUP,
        text=f'Пользователь @{user.username if user.username else user.user_id} добавил ссылку: {message.text}'
        
    )
    
    await state.clear()


@dp.message(F.text)
async def get_hash(message: Message):
    main_post = await Post.get(tag='main')
    await message.answer(main_post.text)


@dp.message(F.video | F.video_note | F.photo | F.audio | F.animation | F.sticker | F.document | F.voice)
async def get_hash(message: Message):
    if (await User.get(user_id=message.from_user.id)).status != 'admin':
        return

    if message.video:
        hashsum = message.video.file_id
    elif message.video_note:
        hashsum = message.video_note.file_id
    elif message.photo:
        hashsum = message.photo[-1].file_id
    elif message.audio:
        hashsum = message.audio.file_id
    elif message.animation:
        hashsum = message.animation.file_id
    elif message.sticker:
        hashsum = message.sticker.file_id
    elif message.document:
        hashsum = message.document.file_id
    elif message.voice:
        hashsum = message.voice.file_id
    else:
        return

    await message.answer(f'<code>{hashsum}</code>')


async def main() -> None:
    await init_db()
    
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())
