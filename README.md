# Web Messenger MVP

Минимальный веб-мессенджер:
- **Backend**: FastAPI + WebSocket
- **Frontend**: HTML/JS
- Авторизация по нику (на этапе WebSocket-подключения)
- Общий чат
- Хранение сообщений в SQLite
- Realtime через WebSocket

## Структура

- `backend/`
- `frontend/`

## Запуск backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Запуск frontend

Откройте `frontend/index.html` в браузере
или поднимите простой сервер:

```bash
cd frontend
python -m http.server 8080
```

После открытия страницы:
1. Введите URL backend (по умолчанию `http://localhost:8000`)
2. Введите ник
3. Пишите сообщения в общий чат
