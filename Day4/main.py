# 실습1
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
#
# app = FastAPI()
#
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept() # Websocket 연결 수락
#     try:
#         while True:
#             data = await websocket.receive_text() # 클라이언트 메세지 수신
#             await websocket.send_text(f"서버 응답: {data}") # 클라이언트에게 응답
#
#     except WebSocketDisconnect:
#         print("연결 해제")

# 실습2
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# import psutil
# import asyncio
#
# app = FastAPI()
#
# @app.websocket("/ws/monitor")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = {
#                 "cpu": psutil.cpu_percent(),
#                 "ram": psutil.virtual_memory().percent
#             }
#             await websocket.send_json(data)
#             await asyncio.sleep(1)
#
#     except WebSocketDisconnect:
#         print("웹소켓 연결 해제")

# 실습3
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# import random
#
# app = FastAPI()
#
# @app.websocket("/ws/game")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#
#     secret_number = random.randint(1, 100)
#     attemps = 0
#     await websocket.send_text("게임 시작합니다. 1-100 사이 숫자를 입력하세요")
#
#     try:
#         while True:
#             # 숫자 받기
#             data = await websocket.receive_text()
#             guess = int(data)
#
#             # 시도 횟수 증가
#             attemps += 1
#
#             # secret number랑 guess 비교
#             if guess < secret_number:
#                 await websocket.send_text("🆙")
#             elif guess > secret_number:
#                 await websocket.send_text("⬇️")
#             else:
#                 await websocket.send_text(f"정답! {attemps}회 시도")
#                 break
#
#             await websocket.send_text(data)
#
#     except WebSocketDisconnect:
#         print("연결 해제")

# 실습4
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
#
# app = FastAPI()
#
# @app.websocket("/ws/{nickname}")
# async def websocket_endpoint(websocket: WebSocket, nickname: str):
#     await websocket.accept()
#     await websocket.send_text(f"{nickname}님 환영합니다.")
#
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await websocket.send_text(f"{nickname}님의 메세지: {data}")
#
#     except WebSocketDisconnect:
#         print("연결 해제")

# 실습5
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for conn in self.active_connections:
            await conn.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/chat/{client_name}")
async def websocket_endpoint(websocket: WebSocket, client_name: str):
    await manager.connect(websocket)

    await manager.broadcast(
        {
            "type": "system",
            "message": f"{client_name}님이 입장하셨습니다"
        }
    )

    try:
        while True:
          data = await websocket.receive_text()
          await manager.broadcast(
              {
                  "type": "chat",
                  "message": data,
                  "sender": client_name
              }
          )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(
            {
              "type": "system",
              "message": f"{client_name}님이 퇴장하셨습니다"
            }
        )