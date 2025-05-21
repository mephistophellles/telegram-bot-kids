from aiogram import Router, F, flags
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, FSInputFile
from openai import AsyncClient
from aiogram.fsm.state import StatesGroup, State

import app.keyboards as kb
import app.database.requests as rq

class Gen(StatesGroup): #Класс для сохранения текста пользователя для генерации
    text_prompt = State()

class Task(StatesGroup): #Класс для сохранения ответов пользователя в викторине
    answers = State()

router = Router()

async def generate(prompt):
     client = AsyncClient(api_key="sk-4sRChGlmloi5gmB6YanfXNYgnHJ320tc",
                    base_url="https://api.proxyapi.ru/openai/v1",)
     chat_completion = await client.chat.completions.create(
        model="gpt-4o", 
        messages=[
        {
            "role": "user",
            "content": prompt
        }])
     return chat_completion.choices[0].message.content.strip()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer_photo(FSInputFile(path="app/media/base-photo.png"), 
                               caption= f"Привет, {message.from_user.full_name}!\n\n<b>Я - бот Лиги Роботов с ИИ!</b>\nВыбери нужный пункт на клавиатуре.", 
                               parse_mode=ParseMode.HTML,
                               reply_markup=kb.student_menu)
    
@router.callback_query(F.data == 'speak')
async def speak(callback: CallbackQuery, state: FSMContext):
     await state.set_state(Gen.text_prompt)
     await callback.message.answer("📝 Отправьте текст запроса к нейросети для генерации текста")

@router.message(Gen.text_prompt)
@flags.chat_action("typing")
async def generate_text(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer("⏳Пожалуйста, подождите немного, пока нейросеть обрабатывает ваш запрос...")
    res = await generate(prompt)
    await mesg.delete()
    await msg.answer(f'{res}')

@router.callback_query(F.data == 'tasks')
async def do_it(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Task.answers)
    await callback.answer()
    await callback.message.answer("Предлагаю поучаствовать в викторине на тему 'Датчики'!")

@router.message(Task.answers)
@flags.chat_action("typing")
async def generate_qa(msg: Message, state: FSMContext):
    pass