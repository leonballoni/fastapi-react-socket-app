import os
import json 

def mock_users():
    path = 'dummy_users.json'
    if os.path.exists(path):
        with open(path, 'r') as user_file:
            return json.load(user_file)
    else:
        return [
         {'username': 'leon',
          'password': 'teste'},
         {'username': 'marcelo',
          'password': 'teste'},
         {'username': 'rodolfo',
          'password': 'teste'},
         {'username': 'gabriel',
          'password': 'teste'},
         {'username': 'guilherme',
          'password': 'teste'},
         {'username': 'victor',
          'password': 'teste'},
         {'username': 'lucasf',
          'password': 'teste'},
         {'username': 'lucasv',
          'password': 'teste'},
         {'username': 'vinicius',
          'password': 'teste'},
        ]


def mock_chats():
    path = 'dummy_chats.json'
    if os.path.exists(path):
        with open(path, 'r') as chat_file:
            return json.load(chat_file)
    else:
        return [
        {'chat_id': 1, "chat": 'sala 1', "owner": 'gabriel', 'messages':
         [{'message_id': 1,
           'username': 'gabriel',
           "message": 'Alguém pode me ajudar?',
           "date": "2024/01/10 10:00:21"
           }]},
        {'chat_id': 2, "chat": 'sala 2', "owner": 'leon', 'messages':
         [{'message_id': 1,
           'username': 'leon',
           "message": 'Oi, tudo bem?',
           "date": "2024/01/10 10:22:21"},
          {'message_id': 2,
           'username': 'marcelo',
           "message": 'Tudo e com você?',
           "date": "2024/01/10 10:23:21"},
          {'message_id': 3,
           'username': 'rodolfo',
           "message": 'eai galera!',
           "date": "2024/01/10 10:24:21"},
          {'message_id': 4,
           'username': 'leon',
           "message": 'Bom d+',
           "date": "2024/01/10 10:25:21"}]}
        ]
