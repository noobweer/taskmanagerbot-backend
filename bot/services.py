import aiohttp
from typing import Optional, Dict, List
from config import *


async def get_or_create_user(telegram_id: int) -> Optional[Dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(AUTH_URL, params={"telegram_id": telegram_id}) as resp:
            if resp.status == 200:
                return await resp.json()
    return None


async def fetch_tasks(token: str) -> List[Dict]:
    headers = {"Authorization": f"Token {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(TASK_URL, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("tasks", [])
    return []


async def create_task(token: str, title: str, due_date: str) -> (bool, str):
    payload = {
        "title": title,
        "description": "Тестовая таска",
        "due_date": due_date,
        "category": "Баги"
    }
    headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(CREATE_TASK_URL, json=payload, headers=headers) as resp:
                data = await resp.json()
                if data.get("is_created"):
                    return True, "✅ Задача создана!"
                return False, f"❌ Ошибка: {data.get('message') or await resp.text()}"
        except Exception as e:
            return False, f"⚠️ Ошибка подключения: {e}"
