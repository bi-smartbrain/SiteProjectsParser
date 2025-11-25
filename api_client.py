import os
import requests
import functools
from typing import Dict, List, Callable
from env_loader import setup_environment

setup_environment()
from config import Settings


def refresh_token_on_401(func: Callable):
    """Декоратор для автоматического обновления токена при 401 ошибке"""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print("Обнаружена 401 ошибка, обновляем токен...")
                if self.refresh_auth_token():
                    return func(self, *args, **kwargs)
            raise

    return wrapper


class APIClient:
    def __init__(self):
        self.settings = Settings()
        self.tokens = self.get_tokens()
        self.auth_token = self.tokens['access']
        self.refresh_token = self.tokens['refresh']
        self.update_headers()

    def update_headers(self):
        """Обновляет заголовки с текущим токеном"""
        self.headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }

    def get_tokens(self):
        """Возвращает access_token и refresh_token"""
        username = os.getenv("SITE_USERNAME")
        password = os.getenv("SITE_PASSWORD")
        auth_url = self.settings.API_AUTH_URL

        response = requests.post(auth_url, json={'email': username, 'password': password})
        response.raise_for_status()
        return response.json()

    def refresh_auth_token(self):
        """Обновляет access token используя refresh token"""
        try:
            # Предполагаем, что endpoint для обновления такой же как для аутентификации
            # или добавляем отдельный URL в настройки
            refresh_url = getattr(self.settings, 'API_REFRESH_URL', self.settings.API_AUTH_URL)

            response = requests.post(refresh_url, json={'refresh': self.refresh_token})

            if response.status_code == 200:
                new_tokens = response.json()
                self.auth_token = new_tokens['access']
                # Сохраняем новый refresh token если он предоставлен, иначе используем старый
                self.refresh_token = new_tokens.get('refresh', self.refresh_token)
                self.update_headers()
                print("Токен успешно обновлен")
                return True
            else:
                print("Не удалось обновить токен, выполняется перелогин")
                return self.full_reauthenticate()
        except Exception as e:
            print(f"Ошибка при обновлении токена: {e}")
            return self.full_reauthenticate()

    def full_reauthenticate(self):
        """Полная переаутентификация по логину и паролю"""
        try:
            self.tokens = self.get_tokens()
            self.auth_token = self.tokens['access']
            self.refresh_token = self.tokens['refresh']
            self.update_headers()
            print("Успешная переаутентификация")
            return True
        except Exception as e:
            print(f"Ошибка переаутентификации: {e}")
            return False

    @refresh_token_on_401
    def get_longlists(self, domain, is_all=True) -> List[Dict]:
        """Парсинг лонг-листов"""
        total_pages = 1
        size = 50
        if is_all:
            counters = requests.get(url=f"https://{domain}.com/api/stage/long-list/counters/",
                                    headers=self.headers, timeout=30)
            counters.raise_for_status()
            total_size = counters.json()['total']
            remainder = 1 if total_size % size > 0 else 0
            total_pages = total_size // size + remainder

        grand_results = []
        for page in range(1, total_pages + 1):
            resp = requests.get(f"https://{domain}.com/api/stage/long-list/?page={page}&size={size}",
                                headers=self.headers, timeout=30)
            resp.raise_for_status()
            results = resp.json()['results']
            print(f"LONG LISTS {domain} - страница {page} из {total_pages} данные получены")
            grand_results += results
        return grand_results

    @refresh_token_on_401
    def get_stages(self, domain, is_all=True) -> List[Dict]:
        """Парсинг вакансий"""
        total_pages = 1
        size = 50
        if is_all:
            counters = requests.get(url=f"https://{domain}.com/api/hr/counts/?forSuperAdmin=true",
                                    headers=self.headers, timeout=30)
            counters.raise_for_status()
            total_size = counters.json()['all_stages_count']
            remainder = 1 if total_size % size > 0 else 0
            total_pages = total_size // size + remainder

        grand_results = []
        for page in range(1, total_pages + 1):
            resp = requests.get(f"https://{domain}.com/api/v2/stage/manager/control/list/?page={page}&size={size}",
                                headers=self.headers, timeout=30)
            resp.raise_for_status()
            results = resp.json()['results']
            print(f"STAGES {domain} - страница {page} из {total_pages} данные получены")
            grand_results += results
        return grand_results