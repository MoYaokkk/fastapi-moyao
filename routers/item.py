from fastapi import APIRouter
# 创建APIRouter对象,指定路由前缀(/users)
router = APIRouter(
    prefix="/items", # 定义商品模块的路由前缀
    tags=["商品管理模块"]
)
@router.get('/')
async def find_all_items():
    return{'message':'查询所有商品'}

@router.get('/{item_id}')
async def find_item_by_id(item_id: int):
    return{'message':f'查询商品id为{item_id}'}
