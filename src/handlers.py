from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db.users import create_user, get_user, get_user_stats
from db.tasks import add_task, get_all_tasks, get_task_by_id, update_task_done, delete_task
from src.keyboards import inline_tasks
router = Router()

class TaskStates(StatesGroup):
    waiting_for_task_text = State()
    waiting_for_done_id = State()
    waiting_for_delete_id = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "Unknown"
    )
    await message.answer(
        f"Привет, {message.from_user.first_name}! Напиши свою первую задачу (≡^∇^≡).\n {user}"
        )


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        '/start - приветствие\n'
        '/help - список команд\n'
        '/add - добавление задач\n'
        '/task - список твоих задач\n'
        '/done - выполнение\n'
        '/delete - удаляет задачу по номеру\n'
        '/stats - статистика задач'
    )

@router.message(Command('add'))
async def cmd_add(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if not user:
        return await message.answer("Сначала напиши /start для регистрации.")
        
    await state.set_state(TaskStates.waiting_for_task_text)
    await message.answer("Введите новую задачу:")

@router.message(TaskStates.waiting_for_task_text)
async def process_add_task(message: Message, state: FSMContext):
    add_task(user_id=message.from_user.id, task_text=message.text)
    
    await state.clear()
    await message.answer(f"Задача '{message.text}' успешно добавлена!")

@router.message(Command('tasks'))
async def cmd_tasks(message: Message):
    user = get_user(message.from_user.id)
    if not user:
        return await message.answer("Сначала напиши /start для регистрации.")
        
    tasks = get_all_tasks(user_id=message.from_user.id)
    
    if not tasks:
        return await message.answer("У тебя пока нет задач. Добавь первую через /add.")
        
    response = "Твой список задач:\n\n"
    for idx, task in enumerate(tasks, start=1):
        status_icon = "✅" if task['done_task'] == 1 else "⬜"
        response += f"{idx}. {status_icon} {task['task_text']} (ID: {task['id']})\n"
        
    await message.answer(response, reply_markup=inline_tasks)

@router.message(Command('done'))
async def cmd_done(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if not user:
        return await message.answer("Сначала напиши /start для регистрации.")
        
    await state.set_state(TaskStates.waiting_for_done_id)
    await message.answer("Введите ID задачи, чтобы отметить её выполненной:")


@router.message(TaskStates.waiting_for_done_id)
async def process_done_task(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Пожалуйста, введите корректное число (ID).")
        
    task_id = int(message.text)
    user = get_user(message.from_user.id)
    task = get_task_by_id(task_id)
    
    if not task or task['user_id'] != user['id']:
        await state.clear()
        return await message.answer("задача не найдена или принадлежит другому пользователю!")
        
    update_task_done(task_id)
    await state.clear()
    await message.answer(f"Задача ID {task_id} переведена в статус выполненной!")


@router.message(Command('stats'))
async def cmd_stats(message: Message):
    user = get_user(message.from_user.id)
    if not user:
        return await message.answer("Сначала напиши /start для регистрации.")
        
    stats = get_user_stats(user_id=message.from_user.id)
    
    if not stats or stats['total'] == 0:
        return await message.answer("У тебя еще нет задач для отображения статистики.")
        
    await message.answer(
        f"Ваша статистика задач:\n"
        f"Всего задач: {stats['total']}\n"
        f"Выполнено: {stats['done'] or 0}\n"
        f"Не выполнено: {stats['not_done'] or 0}"
    )

@router.message(Command('delete'))
async def cmd_delete(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if not user:
        return await message.answer("Сначала напиши /start для регистрации.")
        
    await state.set_state(TaskStates.waiting_for_delete_id)
    await message.answer("Введите системный ID задачи, которую хотите УДАЛИТЬ:")


@router.message(TaskStates.waiting_for_delete_id)
async def process_delete_task(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Пожалуйста, введите корректное число (ID).")
        
    task_id = int(message.text)
    user = get_user(message.from_user.id)
    task = get_task_by_id(task_id)
    
    if not task or task['user_id'] != user['id']:
        await state.clear()
        return await message.answer("задача не найдена или принадлежит другому пользователю!")
        
    delete_task(task_id)
    await state.clear()
    await message.answer(f"🗑 Задача ID {task_id} полностью удалена.")