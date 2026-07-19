from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup, 
                           )

inline_tasks = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Отметить выполненной", callback_data="task_mark_done")
    ]
])