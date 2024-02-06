import uvicorn
from init_app import init_app, FastAPICustomized

app: FastAPICustomized = init_app()

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, access_log=True, port=8000)
