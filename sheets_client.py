import os
import gspread
from config import Settings
from gspread.utils import rowcol_to_a1
from dotenv import load_dotenv
from env_loader import SECRETS_PATH
# from src.utils.logger import setup_logging

# logger = setup_logging()


class GoogleSheetsClient:
    def __init__(self):
        self.settings = Settings()
        self.gc = self.setup_client()

    def setup_client(self):
        """Настройка клиента Google Sheets"""
        service_account_file = os.path.join(SECRETS_PATH, 'service_account.json')
        gc = gspread.service_account(filename=service_account_file)
        return gc


    def add_report_to_sheet(self, spread, sheet, report):
        """Добавляет на лист данные без удаления уже существующих"""
        sh = self.gc.open(spread)
        worksheet = sh.worksheet(sheet)

        # Получить размеры отчета (количество строк и столбцов)
        num_rows = len(report)
        num_cols = len(report[0])

        # Получить диапазон для записи данных
        q_rows = len(worksheet.get_all_values())  # узнаем кол-во уже заполненных на листе строк

        start_cell = rowcol_to_a1(q_rows + 1, 1)
        end_cell = rowcol_to_a1(q_rows + num_rows, num_cols)

        # Записать значения в диапазон
        cell_range = f"{start_cell}:{end_cell}"
        worksheet.update(cell_range, report, value_input_option="user_entered")
        print("Отчет добавлен")


    def write_spread_sheet(self, spread, sheet, report):
        """Перезаписывает лист гугл таблицы"""
        sh = self.gc.open(spread)
        worksheet = sh.worksheet(sheet)
        worksheet.clear()
        print(f"Лист {sheet} в таблице {spread} очищен")

        # Получить размеры отчета (количество строк и столбцов)
        num_rows = len(report)
        num_cols = len(report[0])

        # Получить диапазон для записи данных
        start_cell = rowcol_to_a1(1, 1)
        end_cell = rowcol_to_a1(num_rows, num_cols)

        # Записать значения в диапазон
        cell_range = f"{start_cell}:{end_cell}"
        worksheet.update(report, cell_range, value_input_option="user_entered")

        print("Отчет записан")

    def get_sheet_range(self, spread, sheet, arange):
        """Получает из гугл таблицы диапазон"""

        sh = self.gc.open(spread)
        data = sh.worksheet(sheet).get(arange)
        return data

