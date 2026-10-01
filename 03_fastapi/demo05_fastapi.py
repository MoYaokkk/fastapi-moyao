import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# 请求体了解
# 定义数据模型类,需要继承 BaseModel 的类。
class Item(BaseModel):
  param1: str = None
  param2: str = None

app = FastAPI()

@app.post("/items/")
async def request_method01(item: Item):
  return item

if __name__ == "__main__":
  # 直接在代码中启动uvicorn服务器
  uvicorn.run(
    app="demo05_fastapi:app",    # 指定要运行的FastAPI应用实例
    host="0.0.0.0", # 允许外部访问(本地可通过127.0.0.1或localhost访问)
    port=8000,   # 端口号
    reload=True  # 开发模式：代码修改后自动重启(生产环境需去掉)
)