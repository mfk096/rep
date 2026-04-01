import json
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "chat.db"

app = FastAPI(title="Web Messenger MVP")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_connections: Dict[str, WebSocket] = {}


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with closing(get_db()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/api/messages")
def list_messages(limit: int = 100):
    if limit < 1 or limit > 500:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 500")

    with closing(get_db()) as conn:
        rows = conn.execute(
            """
            SELECT id, nickname, text, created_at
            FROM messages
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    messages = [dict(row) for row in reversed(rows)]
    return {"messages": messages}


def save_message(nickname: str, text: str) -> dict:
    created_at = datetime.now(timezone.utc).isoformat()
    with closing(get_db()) as conn:
        cur = conn.execute(
            "INSERT INTO messages (nickname, text, created_at) VALUES (?, ?, ?)",
            (nickname, text, created_at),
        )
        conn.commit()
        msg_id = cur.lastrowid

    return {
        "id": msg_id,
        "nickname": nickname,
        "text": text,
        "created_at": created_at,
    }


async def broadcast(payload: dict) -> None:
    disconnected = []
    for nickname, ws in active_connections.items():
        try:
            await ws.send_text(json.dumps(payload, ensure_ascii=False))
        except Exception:
            disconnected.append(nickname)

    for nickname in disconnected:
        active_connections.pop(nickname, None)


@app.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    nickname = (websocket.query_params.get("nickname") or "").strip()
    if not nickname:
        await websocket.close(code=1008, reason="Nickname required")
        return

    if nickname in active_connections:
        await websocket.close(code=1008, reason="Nickname already in use")
        return

    await websocket.accept()
    active_connections[nickname] = websocket

    await broadcast({"type": "system", "text": f"{nickname} joined the chat"})

    try:
        while True:
            text = (await websocket.receive_text()).strip()
            if not text:
                continue

            message = save_message(nickname, text)
            await broadcast({"type": "message", "message": message})
    except WebSocketDisconnect:
        pass
    finally:
        active_connections.pop(nickname, None)
        await broadcast({"type": "system", "text": f"{nickname} left the chat"})
