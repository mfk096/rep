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

## Запуск на Windows (PowerShell)

### 1) Backend

```powershell
cd backend
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Если PowerShell блокирует активацию скриптов, выполните:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 2) Frontend

В новом окне PowerShell:

```powershell
cd frontend
py -3 -m http.server 8080
```

Откройте в браузере: `http://localhost:8080`

### 3) Подключение

После открытия страницы:
1. Введите URL backend: `http://localhost:8000`
2. Введите ник
3. Пишите сообщения в общий чат

## Альтернатива: запуск .bat-файлами (Windows)

### Backend

```bat
cd backend
start_backend.bat
```

### Frontend

```bat
cd frontend
start_frontend.bat
```

## Запуск на Linux/macOS

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
python3 -m http.server 8080
```
