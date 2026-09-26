from fastapi import FastAPI
# 创建FastAPI对象
app = FastAPI()

@app.get('/')
async def request_method01():
    return {'message': 'hello fastapi'}


@app.get('/items/{item_id}')
async def request_method02(item_id:int,param:str = None):
    return {'item_id': item_id, 'param': param}