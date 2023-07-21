from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler


def done_task(update: Update, context: CallbackContext) -> None:
    """Получает номер задания в базе 'task_data_base', к которому привязана кнопка.
    Забирает его данные и с помощью них отправляет сообщение ответственному менеджеру
    с информацией и статусом выполнения 'Выполнено!'. Отправляет уведомление об отправке статуса сотруднику. """
    task_id = int(update.callback_query.data[9:])
    context.bot.send_message(chat_id=task_data_base[task_id]['manager_id'],
                             text=f"Сотрудни(к/ца): {task_data_base[task_id]['name']}\n"
                                  f"Задача: {task_data_base[task_id]['task']}\n"
                                  f"Статус: Выполнено!")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Статус выполнения отправлен менеджеру.")


def undone_task(update: Update, context: CallbackContext) -> None:
    """Получает номер задания в базе 'task_data_base', к которому привязана кнопка.
    Забирает его данные и с помощью них отправляет сообщение ответственному менеджеру
    с информацией и статусом выполнения 'Не сделано!'. Отправляет уведомление об отправке статуса сотруднику. """
    task_id = int(update.callback_query.data[11:])
    context.bot.send_message(chat_id=task_data_base[task_id]['manager_id'],
                             text=f"Сотрудни(к/ца): {task_data_base[task_id]['name']}\n"
                                  f"Задача: {task_data_base[task_id]['task']}\n"
                                  f"Статус: Не сделано!")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Статус выполнения отправлен менеджеру.")


def get_status_keyboard_markup(task_id: int) -> InlineKeyboardMarkup:
    """Принимает номер задания 'task_id' и создает Inline клавиатуру с двумя кнопками: 'Выполнено' и 'Не сделано'.
    В 'callback_data' каждой кнопки записывает номер задания 'task_id'. """
    keyboard = [[InlineKeyboardButton("Выполнено", callback_data=f'done_task{task_id}'),
                 InlineKeyboardButton("Не сделано", callback_data=f'undone_task{task_id}')]]
    return InlineKeyboardMarkup(keyboard)


def send_task(tel_id: int, task: str, task_id: int) -> None:
    """Отправляет сообщение с заданием 'task' в телеграм чат сотрудника 'tel_id'
    с прикрепленной Inline клавиатурой созданной с помощью  функции 'get_status_keyboard_markup'."""
    updater.bot.send_message(chat_id=tel_id, text=task, reply_markup=get_status_keyboard_markup(task_id))


def run_module_task_bot() -> None:
    """Запускает модуль 'task_updater.py'. Пытается открыть файл и выполнить его содержимое как исполняемый код.
    Если файл не найден, выводит сообщение "Не удалось найти файл 'task_updater.py'."""
    try:
        with open("task_updater.py") as f:
            code = compile(f.read(), "task_updater.py", "exec")
            exec(code)
    except FileNotFoundError:
        print("Не удалось найти файл 'task_updater.py'.")


def send_new_tasks(update: Update, context: CallbackContext) -> None:
    """Функция выполняет следующие действия:
    1. Проверяет и продолжает выполнение только, если id чата пользователя, запустившего команду '/send_new_tasks',
     есть в списке менеджеров 'managers_id'.
    2. Запускает функцию 'run_module_task_bot'.
    3. Проверяет и продолжает выполнение, если есть новые задания в списке 'new_tasks'(является непустым). Если нет,
     то отправляет менеджеру в чат сообщение с соответствующим уведомлением и завершает выполнение.
    4. Обходит в цикле 'for' список заданий 'new_tasks' и для каждого задания(хранятся в виде словарей) выполняет:
        4.1 добавляет в задание 'new_tasks[i]' пару id чата менеджера с ключем '["manager_id"]',
        4.2 добавляет само задание 'new_tasks[i]' в базу данных 'task_data_base'(является списком словарей),
        4.3 запускает фукцию 'send_task', передавая ей id чата сотрудника 'tel_id', задачу 'task', и будущий id задачи.
    5. Отправляет сообщение в телеграм чат менеджера, что новые задачи успешно отправлены.
    6. Обнуляет список задач 'new_tasks'(делает пустым списком)."""
    if update.message.chat_id in managers_id:
        run_module_task_bot()
        global new_tasks
        if new_tasks:
            for i in range(len(new_tasks)):
                new_tasks[i]["manager_id"] = update.effective_chat.id
                task_data_base.append(new_tasks[i])
                send_task(tel_id=new_tasks[i]['tel_id'], task=new_tasks[i]['task'], task_id=len(task_data_base) - 1)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Новые задачи успешно отправлены.")
            new_tasks = []
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Нет новых задач. Внесите новые задачи в таблицу TaskTable.")


def main() -> None:
    """Запускает телеграм бота(Task_bot) с помощью 'start_polling' до команды об отключении(Ctrl+C) в терминале
    с помощью 'idle'. Также запускаются обработчик команды '/send_new_tasks', вызывающий одноименную функцию,
    и два CallbackQuery обработчика кнопок:
    'Выполнено' - вызывает функцию 'done_task'
    'Не сделано' - вызывает 'undone_task'.
    """
    updater.dispatcher.add_handler(CommandHandler('send_new_tasks', send_new_tasks))
    updater.dispatcher.add_handler(CallbackQueryHandler(done_task, pattern=r'^done_task\d+$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(undone_task, pattern=r'^undone_task\d+$'))
    updater.start_polling()
    print('Bot is working!')
    updater.idle()


updater = Updater("TOKEN") # Здесь должен быть секретный токен телеграм бота.
managers_id = [123456789, ...] # Список id телеграм чатов(int) пользователей, которым предоставляется статус 'менеджер'.
new_tasks = [] # Будет использоваться для работы с новыми заданиями каждый раз после вызова '/send_new_tasks'.
task_data_base = [] # Локальная база данных. В ней будут сохраняться все задания,
                    # загруженные из таблицы в Google Sheets в виде словарей.

if __name__ == "__main__":
    main()
