import time

from config import Settings
from api_client import APIClient
from data_processor import data_processor, sheets_client
from site_parser import parser
from sheets_client import GoogleSheetsClient
from tg_logger import logger


class SiteProjectsParser:
    def __init__(self):
        self.settings = Settings()
        self.api_client = APIClient()
        self.sheets_client = GoogleSheetsClient()

    def run(self):
        """Основной цикл работы приложения"""

        # Сбор новых данных с сайтов
        longlists_report = [['actual_date', 'domain', 'longlist_id', 'stage_url', 'total_count',
                            'project_id', 'stage_id', 'project_name', 'longlist_title']]
        for domain in ["junbrain.com", "junbrain.ru", "engibrain.com", "engibrain.ru"]:
            parsing_results = parser(domain, is_all=True)
            # stages_report = parsing_results['stages_report']
            longlists = parsing_results['longlist_report']
            longlists_report += longlists
        # pprint(longlists_report)
        sheets_client.write_spread_sheet("RecruitTracker", "longlists", longlists_report)
        logger.trace("Обновление завершено успешно..")

        # обработка и запись данных в таблицу
        # data_processor(stages_report, longlists_report)

if __name__ == "__main__":
    while True:
        try:
            tracker = SiteProjectsParser()
            tracker.run()
            time.sleep(60*60*12)
        except Exception as e:
            print(e)
            logger.critical(f"❌ Остановка скрипта SiteProjectsParser, ошибка: {e}")
            time.sleep(60*5)
            logger.info(f"✅ SiteProjectsParser перезапустился")