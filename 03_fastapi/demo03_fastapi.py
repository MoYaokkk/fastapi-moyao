import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/main")
async def request_method02():
    return {"main":"main"}


@app.get("/items/{item_id}")
async def request_method01(item_id):
    return {"item_id":item_id}

if __name__ == '__main__':
    uvicorn.run(
        app="demo03_fastapi:app",
        host="0.0.0.0",
        port=8000,
        reload=True #代码修改后自动重启
    )
