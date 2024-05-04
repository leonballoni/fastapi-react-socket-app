# fastapi-react-socket-app

**OBS**: por motivos que não compreendo ainda, o websocket não executa em navegadores Chrome.

O exemplo faz uso de Python, FastAPI, Poetry e Python-socketio como base para servidor no Backend e Javascript, React, Node e Socket.io para o cliente no Frontend. Outros pacotes foram utilizados e estão descritos nos pacotes de gerenciamento de bibliotecas e versões de ambas as linguagens


**Objetivos** 
- Ter um ambiente (servidor e cliente) funcional e minimalista com operação de conectar, chats e mensagens em chat operando.
- Servir de base para futuros desenvolvimentos com uso da interface de websockets  

**Colaboradores**
- Elaborada por Leon Balloni com apoio de Yuri Mutti e Renan Yudi para Frontend 


**Ferramentas**

- [Python](https://www.python.org/)
[Poetry](https://python-poetry.org/);
[FastAPI](https://fastapi.tiangolo.com/), e;
[python-socketio](https://python-socketio.readthedocs.io/en/stable/).

- [JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript) 
[React](https://react.dev/);
[Node.js](https://nodejs.org/en/download/current);
[Socket.io](https://websocket.io/), e;
[React Developer Tools](https://addons.mozilla.org/en-US/firefox/addon/react-devtools/).

**base de front criado com NPX**
```shell
npx create-react-app APP_NAME
```

## Como iniciar

### Servidor

1. Instale versão python 3.10 ou maior; 
```shell
sudo apt-get install python3.10
```

2. Instale o ambiente virtual com poetry;
```python
pip install poetry 
```
> O caminho em seu terminal deve contar o pyproject.toml
```python
poetry install 
```
> Confira se o ambiente virtual (Venv) foi ativado em seu terminal e configure o interpretador de sua IDE

> para exigir os pacotes instalados
```sh
poetry show
```

3. Inicialize o servidor 
> Terminal:
```shell
python3 server/main.py  
```
> IDE

Execute arquivo main.py

### Cliente

1. Instale o Node.js
```sh
sudo snap install node --classic 
```
2. Confira o gerenciador de pacotes
```sh
npm - v 
```
e
```sh
npx -v 
```
3. Instale os pacotes do cliente (pasta client)
```sh
npm install 
```
4. inicialize o cliente (pasta client)
> Terminal:
npm start

> o cliente será hospedado na porta 3000 (utilize outro navegador que Chrome para cosneguir interagir)

## Conceitos

### Para Leigos

Pense nos Websockets como portões (*Gates*) que possibilitam comunicação entre diferentes processos na mesma ou entre máquinas diferentes. De certa forma, websocket pode ser entendido como dois dutos que transferem fluídos (dados) continuamente sem esperar necessariamente pelo retorno do outro, gerando essa percepção de fluidez e continuidade.  

Considere a analogia do ping-pong onde diferentemente do padrão onde mandamos algo e esperamos uma resposta seja ela qual for e por x tempo, as interações são rápidas e quase intermitente e exigem respostas quase que instâneas. 


### Para Devs

Websocket ou websockets são interfaces de conexão bidirecional onde há comunicação contínua entre o cliente e o servidor a partir de um IP único e um identificador (SID) da conexão. 

A comunicação é via **pacotes** que transmitem a comunicação na rede de computadores (mensagem) e destinados para um **endpoint** após seguir um **IP** e **Porta** de um aparelho ligado a rede.  

Sua operação é realizada pela associação dos endereços IP e suas portas entre o requisitor e o receptor. Isso possibilita que uma máquina reconheça a outra e compartilhem a mesma conexão para transmissão de dados sem gerar bloqueios no websocket para outras conexões de outros IPs.  

#### Eventos

É por meio dessa conexão e do gerenciamento de eventos que essa interface opera. Diferentemente das requisições onde se solicita algo, obtem-se uma resposta e a conexão é encerrada, neste caso, a conexão é mantida na escuta por eventos emitidos pelo cliente. Por meio desses eventos, o servidor emite outros eventos e constroi essa interação de fluidez contínua que uma aplicação como Chat devem gerar. 

## Estrutura do Servidor

    .
    ├── init_app.py -> Rotas HTTPs e Websockets
    ├── main.py -> Inicializador do servidor
    ├── mocked_data.py -> Dados falsos utilizados durante a app
    ├── schemas.py -> Esquemas pydantic para validar e gerar o conjunto de rotas e dados utilizados nos websockets
    └── socket_client.py -> Cliente inicializador do websocket dentro do FastAPI.


## Estrutura do Cliente-servidor
    ├── node_modules
    ├── .env
    ├── package.json
    ├── package-lock.json
    ├── public
    │   ├── index.html
    │   ├── manifest.json
    │   └── robots.txt
    ├── README.md
    └── src
        ├── App.css
        ├── App.js
        ├── components
        │   ├── Init.js
        │   ├── LoginModal.js
        │   ├── SocketComponents.js
        │   └── Socket.js
        ├── index.css
        ├── index.js
        └── reportWebVitals.js

## Pontos a melhorar

1. Modificar formato de atualização do status do usuário
2. Separar em mais componentes o frontend (problema de mudança de chats)
3. Aprimorar a separação de módulos dentro do backend
4. Melhorar interface visual criada no css

Longe de ser uma aplicação final e perfeita, há vários pontos para aperfeiçoar. Contudo, espero que isso ajude pessoas em situações similares à construirem aplicações utilizando esse com maior facilidade. 


## Observações

(Docs para futuras implementações)[https://www.asyncapi.com/]

(Conceitos de Websockets em Python)[https://www.datacamp.com/tutorial/a-complete-guide-to-websocket-programming-in-python]

(Fastapi websocket desenvolvido fez uso de parte do desenvolvido neste repositório)[https://github.com/pyropy/fastapi-socketio]

(Vídeo tutorial com flask e socketio)[https://www.youtube.com/watch?v=AMp6hlA8xKA&ab_channel=PrettyPrinted]

(React Crash course)[https://www.youtube.com/watch?v=w7ejDZ8SWv8]
