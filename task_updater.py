import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Это дополнительный модуль для телеграм Task_bot. Скрипт выполняет подключение к обозначенной таблице в Google Sheets.
# Проходит аутентификацию. Использует для этого название таблицы и JSON-файл с ключами доступа.
# Затем при наличии новых строк загружает их из таблицы и записывает в виде словарей в переменную(list) 'new_tasks'.
# Сохраняет информацию о последней загруженной строке в файле 'last_row.txt'.

if __name__ == '__main__':
    # Путь к JSON-файлу с ключами доступа.
    json_keyfile = 'secret_key.json'

    # Устанавливает область доступа для использования Google Sheets API.
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # Аутентификация с помощью учетных данных.
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(credentials)

    # Открывает таблицу по ее названию. Легко позволяет переподключать бота к разным таблицам Google Sheets.
    spreadsheet_name = 'Название вашей таблицы Google Sheets'
    sheet = client.open(spreadsheet_name).sheet1

    # Проверяет, есть ли файл с номером последней загруженной строки.
    # Если есть, использует его как номер первой строки для загрузки.
    last_row_file = 'last_row.txt'
    if os.path.exists(last_row_file):
        with open(last_row_file, 'r') as f:
            last_row = int(f.read())
    else:
        last_row = 1  # Если файл не существует, начинает с первой строки таблицы.

    # Получает общее количество строк в таблице.
    total_rows = len(all_records := sheet.get_all_records())

    # Проверяет, есть ли новые строки для загрузки.
    if total_rows >= last_row:
        while True:
            # Получает список всех строк в таблице, начиная с last_row.
            rows = all_records[last_row - 1:]

            # Если нет новых строк, завершает цикл.
            if not rows:
                break

            # Добавляет новые строки в переменную new_records в виде словарей.
            global new_tasks
            new_tasks.extend(rows)

            # Обновляет last_row для следующей загрузки.
            last_row += len(rows)

        # Сохраняет номер последней загруженной строки в файл.
        with open(last_row_file, 'w') as f:
            f.write(str(last_row))

    # Выводит информацию об успешном выполнении скрипта. Можно использовать для дебаггинга или отключить.
    print("Скрипт из модуля task_updater.py был выполнен!")
