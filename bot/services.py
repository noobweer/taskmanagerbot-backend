import aiohttp
from typing import Optional, Dict
from config import AUTH_URL


async def get_or_create_user(telegram_id: int) -> Optional[Dict]:
    async with aiohttp.ClientSession() as session:
        params = {"telegram_id": telegram_id}
        async with session.get(AUTH_URL, params=params) as response:
            if response.status != 200:
                return None

            try:
                data = await response.json()
                if data.get("success", True):
                    return data
            except Exception as e:
                print(f"Ошибка при парсинге JSON: {e}")
                return None

    return None


async def fetch_tasks(token: str) -> list:
    if not token:
        print("❌ Токен отсутствует")
        return []

    headers = {"Authorization": f"Token {token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get("http://taskmanager-backend:8000/api/tasks/", headers=headers) as response:
            if response.status == 401:
                print("❌ Неавторизованный доступ")
                return []
            elif response.status != 200:
                print(f"⚠️ Ошибка ответа: {response.status}")
                return []
            return await response.json()