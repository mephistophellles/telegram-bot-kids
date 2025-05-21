from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder

student_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📚 Задания", callback_data="tasks")],
        [InlineKeyboardButton(text="🧠 Поговорить с ИИ", callback_data="speak"), InlineKeyboardButton(text="🏆 Мой профиль", callback_data="profile")],
        [InlineKeyboardButton(text="📅 Расписание", callback_data="raspisanie")]
    ]
)
