import time

from config import Settings
from api_client import APIClient
from data_processor import data_processor
from site_parser import parser
from sheets_client import GoogleSheetsClient


class RecruitmentTracker:
    def __init__(self):
        self.settings = Settings()
        self.api_client = APIClient()
        self.sheets_client = GoogleSheetsClient()

    def run(self):
        """Основной цикл работы приложения"""

        # Сбор новых данных с сайтов
        parsing_results = parser()
        stages_report = parsing_results['stages_report']
        longlists_report = parsing_results['longlists_report']

        # обработка и запись данных в таблицу
        data_processor(stages_report, longlists_report)

if __name__ == "__main__":
    while True:
        try:
            tracker = RecruitmentTracker()
            tracker.run()
            time.sleep(60*60*24*7)
        except Exception as e:
            print(e)
            time.sleep(3)
            tracker = RecruitmentTracker()
            tracker.run()