### **Тестовое задание: Telegram бот для управления задачами ToDo List 🤠**

- Ознакомиться с результатом можно по репозиторию или через демо-версии в боте по ссылке: 
- [Нажми на меня](https://t.me/todomanager_robot)

<img src="https://i.imgur.com/SGkhiQm.png" alt="скрин" width="200"/>

#### 🚀 Запуск проекта
- Контейнеризация настроена через docker-compose, все сервисы поднимаются одной командой:
```shell
docker-compose up --build
```

#### Кратко об архитектуре проекта и запуске

<img src="https://i.imgur.com/XWl1h1D.png" alt="скрин" width="300"/>

1. 📲 **Взаимодействие пользователя**

    Пользователь пишет боту в Telegram.
    Бот с помощью aiogram отображает меню, принимает команды, вызывает API-запросы к Django.


2. 🧠 Обработка задач

    Django (taskmanager-backend) обрабатывает запросы: CRUD операции с категориями и тасками, а также авторизация пользователя. Также есть django админ-панель через которую удобно взаимодействовать с данными.
    <img src="https://i.imgur.com/x0XGgac.png" alt="скрин" width="300"/>


3. 📬 Фоновая обработка (Celery)

    Отдельный Celery-воркер следит за сроками задач и отправляет уведомления, если они просрочены.
    Beat запускает периодическую проверку (по расписанию).


4. 💾 Хранение данных

    Все задачи, категории и пользователи Telegram хранятся в PostgreSQL.
    Redis используется как брокер задач (для Celery/Beat).

#### Кратко про основные трудности и их решениях

1. - **Проблема:** Ограничение PK для основных сущностей
   - **Решение:** Для PK тасок используется ULID. Он дает надёжность и уникальность, короче UUID (26 символов против 36).


2. - **Проблема:** Уведомлять пользователя о дедлайне таски
   - **Решение:** Запущен celery beat, который периодически триггерит задачи на проверку сроков и отправку уведомлений в Telegram.


3. - **Проблема:** Синхронизация времени при валидации дедлайнов
   - **Решение:** Использовано timezone.make_aware() и проверка с timezone.now() для корректной обработки времён с учётом часовых поясов


4. - **Проблема:** Аутентификация пользователей Telegram
   - **Решение:** При первом сообщении бот регистрирует Telegram ID пользователя через /api/telegram-login/, и возвращает токен. Далее он используется в заголовках Authorization в запросах API