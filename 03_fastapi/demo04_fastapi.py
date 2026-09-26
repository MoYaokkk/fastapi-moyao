import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get('/items')
async def request_method01(param1:str=None,param2:str=None):
    return {'param1':param1,'param2':param2}

if __name__ == '__main__':
    uvicorn.run(
        app='demo04_fastapi:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )