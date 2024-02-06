from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from socket_client import SocketManager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
import sys
from loguru import logger
import pytz
import json
from schemas import Messages, Chats, UserAuth
from mocked_data import mock_users, mock_chats


logger.add(sys.stderr, colorize=True,
           format="<yellow>{time}</yellow> {level} <green>{message}</green>",
           filter="sockets", level="INFO")


dummy_users = mock_users()

dummy_chats = mock_chats()


# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: list[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)


class FastAPICustomized(FastAPI):
    '''FastAPI interceptor build to integrate seamlessly the SocketManager class and other features

    Added Features

    ----

        - static_files_disabled: dict -> Create a dict to mount a staticfile for interface features
        - socket_client_enabled: bool -> Enable socket-io (bidirectional comm) feature

    ----

    '''
    def __init__(self,
                 static_files_disabled: dict = {'status': False,
                                                'directory': 'front',
                                                'name': 'static'},
                 socket_client_enabled: bool = True,
                 *args, **kwargs):
        # self.conn_manager = ConnectionManager()
        super().__init__(*args, **kwargs)
        if socket_client_enabled:
            self.sio = SocketManager(app=self)
        if static_files_disabled.get('status'):
            self.mount('/static',
                       StaticFiles(directory='src/interface'),
                       name='static')


class InitApp:

    def __init__(self, app: FastAPICustomized):
        # Simulando os dados do user em banco
        self.users_logged = {}
        self.connected_users = {}
        self.rooms = {}
        self.init_http_requests(app)
        self.init_socket(app)
        self.app = self.init_middleware(app)

    def init_http_requests(self, app: FastAPICustomized) -> FastAPICustomized:
        @app.get('/')
        async def home():
            return {'status': 'server online'}

        @app.get('/users')
        async def get_users():
            return dummy_users

        @app.get('/chats')
        async def get_chats(chat_id: int = None):
            if chat_id:
                for chat in dummy_chats:
                    if chat.get('chat_id') == chat_id:
                        return chat
            return dummy_chats

        @app.post('/chats')
        async def create_chat(chat: Chats):
            for chats in dummy_chats:
                if chats.get('chat_id') == chat.chat_id:
                    return Response(status_code=401, content='chat id already registered')
            last_chat_id = dummy_chats[-1].get('chat_id') + 1
            chat.chat_id = last_chat_id
            dummy_chats.append(chat.model_dump())
            with open('dummy_chats.json', 'w') as chat_file:
                json.dump(dummy_chats, chat_file)
            return dummy_chats

        @app.get('/chat/messages')
        async def get_messages(chat_id: int):
            for chats in dummy_chats:
                if chats.get('chat_id') == chat_id:
                    return chats.get('messages')
            return Response(status_code=400, content='No chat found')

        @app.post('/chat/messages')
        async def add_message(chat_id: int, message: Messages):
            for i, chats in enumerate(dummy_chats):
                if chats.get('chat_id') == chat_id:
                    last_msg_id = chats.get('messages')[-1].get('message_id') + 1
                    message.message_id = last_msg_id
                    chats.get('messages').append(message.model_dump())
                    dummy_chats[i].update({'messages': chats.get('messages')})
            with open('dummy_chats.json', 'w') as chat_file:
                json.dump(dummy_chats, chat_file)
            return dummy_chats[i]

        @app.post('/auth')
        async def mock_auth(user_auth: UserAuth):
            for user in dummy_users:
                if user_auth.username == user.get('username'):
                    logger.info(f'User found {user_auth.username}')
                    if user_auth.password == user.get('password'):
                        logger.info(f'User Logged {user_auth.username}')
                        return Response(status_code=200,
                                        content=str({'username': user_auth.username,
                                                     'message': 'user logged'}))
                    msg = "Wrong user or password"
                    logger.warning(msg)
                    return Response(status_code=401, content=msg)
            msg = "User does not exist"
            logger.warning(f"{msg} {user_auth}")
            return Response(status_code=401, content=msg)
        # return app
        
    def init_socket(self, app: FastAPICustomized) -> FastAPICustomized:


        @app.sio.on('connect')
        async def connect(sid, *args, **kwargs):
            await app.sio.emit("load_rooms", [{'chat_id': chat.get("chat_id"),
                                               'chat': chat.get("chat")} for chat in dummy_chats])
            logger.warning(f"Conectou!: {sid}")

        @app.sio.on('disconnect')
        async def disconnection(sid, *args, **kwargs):
            # await app.sio.emit("users_connected", dummy_chats)
            logger.warning(f"Desconectou!: {sid}")

        @app.sio.event
        async def status_user(sid, *args, **kwargs):
            users = []
            for arg in args:
                if arg.get('status') == 'off' and self.users_logged.get(sid):
                    self.users_logged.pop(sid)
                if arg.get('status') == 'on':
                    self.users_logged.update({sid:
                                             {"status": arg.get('status'),
                                              "user": arg.get('user')}
                                              })
            for key in self.users_logged.keys():
                users.append({**self.users_logged.get(key), **{'sid': sid}})
            await app.sio.emit("users_connected", users)

        @app.sio.event
        async def status_room(sid, *args, **kwargs):
            for arg in args:
                if arg.get('chat_id'):
                    for chat in dummy_chats:
                        if chat.get('chat_id') == arg.get('chat_id'):
                            return chat
            logger.warning("Status room")
            return dummy_chats
        
        @app.sio.on("load_room")
        async def load_room(sid, *args, **kwargs):
            logger.warning('Loading a room ', args)
            for arg in args:
                for chat in dummy_chats:
                    if arg.get('chat_id') == chat.get('chat_id'):
                        await app.sio.emit('join_room', {'Room': chat})
                    else:
                        continue
                else:
                    break

        @app.sio.on('join_room')
        async def join_room(sid, *args, **kwargs):
            logger.warning(f"user {args[0].get('user')} entered the room {args[0].get('chat')}")

        @app.sio.on('left_room')
        async def left_room(sid, *args, **kwargs):
            logger.warning(f"user {args[0].get('user')} left the room {args[0].get('chat')}")

        @app.sio.on('send_message')
        async def message(sid, *args, **kwargs):
            for arg in args:
                for chat in dummy_chats:
                    if arg.get('chat_id') == chat.get('chat_id'):
                        last_msg_id = chat.get('messages')[-1].get('message_id') + 1
                        new_msg = Messages(message_id=last_msg_id,
                                           username=arg.get('username'),
                                           message=arg.get('message')).model_dump()
                        chat.get('messages').append(new_msg)
                        new_chat = Chats(chat_id=chat.get('chat_id'),
                                         chat=chat.get('chat'),
                                         owner=chat.get('owner'),
                                         messages=chat.get('messages')).model_dump()
                        new_chat.update({'owner': chat.get('owner')})
                        await app.sio.emit('send_message', {"newMessage": new_msg})
                        # with open('dummy_chats.json', 'w') as chat_file:
                        #     json.dump(dummy_chats, chat_file)
                    else:
                        continue
                else:
                    break

        # @app.websocket("/ws")
        # async def websocket_endpoint(websocket: WebSocket):
        #     await app.conn_manager.connect(websocket)
        #     try:
        #         while True:
        #             data = await websocket.receive_text()
        #             await app.conn_manager.send_personal_message(f"Escreveu: {data}",
        #                                                          websocket)
        #             # await manager.broadcast(f"Client #{client_id} says: {data}")
        #     except WebSocketDisconnect:
        #         app.conn_manager.disconnect(websocket)
        #         # await manager.broadcast(f"Client #{client_id} left the chat")
        # return app

    def init_middleware(self, app: FastAPICustomized):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],)
        return app


def init_app(*args, **kwargs) -> FastAPICustomized:
    app = FastAPICustomized(*args, **kwargs)
    init_app = InitApp(app)
    return init_app.app
