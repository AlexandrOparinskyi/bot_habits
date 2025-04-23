from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

from config import load_config

# Укажи путь к файлу JSON с ключом сервисного аккаунта
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_file(
    'google_sheets_config.json', # Замени на актуальный путь
    scopes=SCOPES
)

# Авторизация с использованием учетных данных сервисного аккаунта
gc = gspread.service_account(filename='google_sheets_config.json', scopes=SCOPES)

config = load_config()

# Открывает нужную таблицу
spreadsheet = gc.open_by_key(config.google_sheet.token)

# Открываем первый лист
worksheet = spreadsheet.sheet1

PRESENT_DATA = {
    True: ("Да", (0, 1, 0)),
    False: ("Нет", (1, 0, 0))
}


async def add_info_for_sheet(username: str, present: bool) -> None:
    now = datetime.now()
    date_to_check = now.strftime("%d.%m.%Y")

    users = worksheet.row_values(1)
    try:
        username_column = users.index(username) + 1
    except ValueError:
        username_column = len(users) + 1
        worksheet.update_cell(1, username_column, username)

    dates = worksheet.col_values(1)
    try:
        date_row = dates.index(date_to_check) + 1
    except ValueError:
        date_row = len(dates) + 1
        worksheet.update_cell(date_row, 1, date_to_check)

    worksheet.update_cell(date_row,
                          username_column,
                          PRESENT_DATA[present][0])
