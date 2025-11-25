import pandas as pd
from sheets_client import GoogleSheetsClient
sheets_client = GoogleSheetsClient()
spread = "RecruitTracker"

def data_processor(stages_report, longlists_report):
    #резервная запись новых данных на листы stages_new и longlists_new
    sheets_client.write_spread_sheet(spread, "stages_new", stages_report)
    sheets_client.write_spread_sheet(spread, "longlists_new", longlists_report)

    # Получение старых данных из гугл-таблицы
    old_stages_report = sheets_client.get_sheet_range(spread, "stages", "A:Z")
    old_longlists_report = sheets_client.get_sheet_range(spread, "longlists", "A:Z")

    # резервная запись старых данных на листы stages_old и longlists_old
    sheets_client.write_spread_sheet(spread, "stages_old", old_stages_report)
    sheets_client.write_spread_sheet(spread, "longlists_old", old_longlists_report)


    # создаем датафреймы на основе новых данных, которые мы спарсили с сайта
    stages_df = pd.DataFrame(stages_report[1:], columns=stages_report[0])
    longlists_df = pd.DataFrame(longlists_report[1:], columns=longlists_report[0])

    # создаем объединенный реестр новых данных, объединяя датафреймы stages и longlists
    stages_df = stages_df.merge(
        longlists_df[['stage_url', 'longlist_id', 'longlist_title', 'total_count']],
        on='stage_url',
        how='left'
        ).fillna({'total_count': 0})
    stages_df['total_count'] = stages_df['total_count'].fillna(0).astype('int64')
    stages_df['longlist_id'] = stages_df['longlist_id'].fillna(0).astype('int64')


    # создаем датафреймы на основе старых данных
    old_stages_df = pd.DataFrame(old_stages_report[1:], columns=old_stages_report[0])
    old_longlists_df = pd.DataFrame(old_longlists_report[1:], columns=old_longlists_report[0])

    # создаем объединенный реестр из старых данных
    old_stages_df = old_stages_df.merge(
            old_longlists_df[['stage_url', 'longlist_id', 'longlist_title', 'total_count']],
            on='stage_url',
            how='left'
        ).fillna({'total_count': 0})
    old_stages_df['total_count'] = old_stages_df['total_count'].fillna(0).astype('int64')
    old_stages_df['longlist_id'] = old_stages_df['longlist_id'].fillna(0).astype('int64')


    # присоединяем колонку с количеством откликом из старого реестра к новому stage_df
    # в качестве колонки pre_total_count по ключу longlist_id удаляя из старого реестра строки, в которых
    # longlist_id = 0 (по факту нет лонг листа у вакансии)

    old_stages_unique = old_stages_df[['longlist_id', 'total_count']].drop_duplicates('longlist_id')
    new_stages_df = stages_df.merge(
            old_stages_unique.rename(
                columns={'total_count': 'pre_total_count'}
            ),
            on='longlist_id',
            how='left'
        ).fillna({'total_count': 0})
    new_stages_df['pre_total_count'] = new_stages_df['pre_total_count'].fillna(0).astype('int64')


    # Запись нового реестра в гугл-таблицу
    new_stages_df = new_stages_df.fillna('')
    reg_report = [new_stages_df.columns.tolist()] + new_stages_df.values.tolist()
    sheets_client.write_spread_sheet(spread, "py_reg", reg_report)

    # перезаписываем листы stages и longlists новыми данными из stages_report и longlists_report
    sheets_client.write_spread_sheet(spread, "stages", stages_report)
    sheets_client.write_spread_sheet(spread, "longlists", longlists_report)