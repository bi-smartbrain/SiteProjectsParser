import pandas as pd
from datetime import datetime as dt
from api_client import APIClient
api_client = APIClient()


def create_longlists_report(longlists, domain):
    report = []
    for item in longlists:
        today = dt.today().strftime('%Y-%m-%d')
        stage_url = (f"https://{domain}.com/account/all-projects/project/{item['stage']['project_id']}"
                     f"?vacancyId={item['stage']['id']}")
        report_row = [
            today,
            domain,
            item['id'],
            stage_url,
            item['total_count'],
            item['stage']['project_id'],
            item['stage']['id'],
            item['stage']['name'],
            item['title'],
        ]
        report.append(report_row)

    report_df = pd.DataFrame(report[1:], columns=report[0])
    report_df = report_df.drop_duplicates()
    report = [report[0]] + report_df.values.tolist()
    return report


longlist_example = {
              'default_for': 'mailed',
              'id': 7499,
              'initial_count': 0,
              'interview_count': 0,
              'is_rate_confirmation_needed': False,
              'pending_count': 0,
              'position': None,
              'reference_id': 'wXNwENx',
              'response_count': 0,
              'responsible': {'first_name': 'Ваш',
                              'id': 'AoOvM6K',
                              'last_name': 'менеджер',
                              'photo': {'original': '/upload/user/2020/09/bizw.jpg',
                                        'webp200': '/upload/CACHE/images/user/2020/09/bizw/c9fcf9f0543c92efe89a138cef39767f.webp',
                                        'webp32': '/upload/CACHE/images/user/2020/09/bizw/05285dd5b0e962cf0dca008f20acd861.webp',
                                        'webp320': '/upload/CACHE/images/user/2020/09/bizw/f17f5693e4922a229b0cef998303202c.webp',
                                        'webp64': '/upload/CACHE/images/user/2020/09/bizw/2f78854bd9b804030d29e2a73e10c988.webp',
                                        'x200': '/upload/CACHE/images/user/2020/09/bizw/a3b9de82dd245a234208c479d9729934.jpg',
                                        'x32': '/upload/CACHE/images/user/2020/09/bizw/69a12f8bed7fb5f93319a226d0157357.jpg',
                                        'x320': '/upload/CACHE/images/user/2020/09/bizw/5c5e10b5138e963abbaec8b8ea95e2a3.jpg',
                                        'x64': '/upload/CACHE/images/user/2020/09/bizw/da216282397925faa79360cab3c58e63.jpg'},
                              'role': 'manager_rubrain'},
              'shortlist_hash': 'v9MXqAl',
              'stage': {'id': 4924,
                        'name': 'Full-stack developer',
                        'project_id': 8528},
              'status': 'active',
              'title': 'Отклики кандидатов на проект “Full-stack developer“',
              'total_count': 1,
              'unread_messages_count': 0}


def create_stages_report(stages, domain):
    report = []
    for stage in stages:
        today = dt.today().strftime('%Y-%m-%d')
        stage_url = f"https://{domain}.com/account/all-projects/project/{stage['project']}?vacancyId={stage['id']}"
        report_row = [
            today,
            domain,
            stage_url,
            stage['id'],
            stage['name'],
            stage['created'][:10],
            stage['status'],
            stage['currency'],
            stage['priority'],
            stage['project'],
            stage['private_ru'],
            stage['private_en'],
        ]
        report.append(report_row)

    report_df = pd.DataFrame(report[1:], columns=report[0])
    report_df = report_df.drop_duplicates()
    report = [report[0]] + report_df.values.tolist()
    return report


stage_example = {
            "id": 4969,
            "name": "Content manager (filling out product cards)",
            "slug": "content-manager-filling-out-product-cards",
            "budget": None,
            "budget_description": "By mutual agreement",
            "closed_at": None,
            "closed_message": None,
            "created": "2025-11-19T10:01:23.399747+03:00",
            "currency": "rub",
            "customer": {
                "id": "Bo8rXW4",
                "reference_id": "Bo8rXW4",
                "first_name": None,
                "last_name": None,
                "company": None
            },
            "customer_state": "search",
            "has_unconfirmed_rate": False,
            "last_mailing": "2025-11-19T10:20:58.058969+03:00",
            "last_mailing_count": 11,
            "manager": {
                "id": "34rwQO6",
                "reference_id": "34rwQO6",
                "first_name": "Aglaya",
                "last_name": "Oleynikova",
                "company": None
            },
            "new_applies_count": 0,
            "new_messages_count": 0,
            "positions_count": 1,
            "priority": "high",
            "project": 8568,
            "status": "search",
            "publishing_params": [
                "remote",
                "project-time",
                "full-time",
                "part-time"
            ],
            "taken_positions_count": 0,
            "vacancy_duration": "1 мес.",
            "vacancy_start": None,
            "private_ru": False,
            "private_en": False
        }


def parser(domain, is_all=True):
    """Парсинг данных с корпоративных сайтов"""
    stages_report = [['actual_date', 'domain', 'stage_url', 'stage_id', 'stage_name', 'stage_created',
                      'stage_status', 'currency', 'priority', 'project_id', 'private_ru', 'private_en']]



    # stages = api_client.get_stages(domain=domain, is_all=is_all)
    longlists = api_client.get_longlists(domain=domain, is_all=is_all)


    # stages_report += create_stages_report(stages, domain)
    longlist_report = create_longlists_report(longlists, domain)

    result = {
        # 'stages_report': stages_report,
        'longlist_report': longlist_report,
    }

    return result