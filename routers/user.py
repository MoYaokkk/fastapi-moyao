from fastapi import APIRouter
# 创建APIRouter对象,指定路由前缀(/users)
router = APIRouter(
    prefix="/users", # 定义用户模块的路由前缀
    tags=["用户管理模块"]
)
@router.get('/')
async def find_all_users():
    return{'message':'查询所有用户'}

@router.get('/{user_id}')
async def find_user_by_id(user_id: int):
    return{'message':f'查询用户id为{user_id}'}
