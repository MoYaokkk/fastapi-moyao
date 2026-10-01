from fastapi import FastAPI
import uvicorn
# 创建FastAPI对象
app = FastAPI()

@app.get('/')
async def request_method01():
    return {'message': 'hello fastapi'}


@app.get('/items/{item_id}')
async def request_method02(item_id:int,param:str = None):
    return {'item_id': item_id, 'param': param}

if __name__ == '__main__':
    uvicorn.run(
        app='demo02_fastapi:app',
        host='127.0.0.1',
        port=8000,
        reload=True # 代码修改后自动重启,好像并不是
    )