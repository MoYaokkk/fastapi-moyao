import asyncio

async def method():
    print('协程方法开始执行')
    # 模拟一个耗时操作,让当前协程挂起,此时其他协程可以执行
    await asyncio.sleep(2)
    print('协程方法结束')


if __name__ == '__main__':
    # 调用method方法,得到一个协程对象
    res = method()

    # 真正执行协程
    asyncio.run(res)