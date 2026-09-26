from fastapi import FastAPI
from routers import item, user
import uvicorn

app = FastAPI(title="路由分发")

# 挂载用户模块的路由
app.include_router(user.router)

# 挂载商品模块的路由
app.include_router(item.router)


# 给主程序定义一个路由
@app.get("/")
async def index():
    return {"message": "欢迎访问主页面"}


if __name__ == "__main__":
    uvicorn.run(
        app="demo01_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )