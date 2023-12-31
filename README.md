# PTB
Алгоритм работы Task_bot:

Реализованные пункты:
1. Менеджер заполняет строки (задания для сотрудников) в Google Sheets.
2. Менеджер запускает команду "/send_new_tasks" в Telegram-боте.
3. Главный модуль ("Task_bot") на Python запускает модуль "task_updater" и получает из него доступ к переменной "new_tasks".
4. Скрипт при помощи обхода в цикле по "new_tasks" рассылает задачи сотрудникам, прикрепляет кнопки о статусе выполнения задания ("Выполнено", "Не сделано") и уведомляет менеджера о том, что задачи поставлены.
5. Сотрудники нажимают на кнопки для передачи статуса. Они получают уведомления, что менеджер получил статус. Менеджер получает уведомление о статусе выполнения.

Возможности для расширения функционала:
1. На каждую задачу выставляется дедлайн (заполняется менеджером в таблице). Если срок выполнения задачи истек, а сотрудник не отправил статус выполнения задачи нажатием на кнопку, то менеджер получает уведомление об игнорировании задачи. Сотрудник также может получать уведомление о невыполненной в срок задаче. При необходимости можно блокировать кнопки передачи статуса после прохождения дедлайна.
2. Есть возможность сделать автоматическое заполнение исходной таблицы в Google Sheets статусами (например: "Выполнено", "Не сделано", "В работе", "Проигнорировано").
