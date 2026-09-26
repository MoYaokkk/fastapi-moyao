import asyncio

async def method01():
    print('协程方法method01开始执行')
    # 模拟一个耗时操作,让当前协程挂起,此时其他协程可以执行
    await asyncio.sleep(2)
    print('协程方法method01结束')

async def method02():
    print('协程方法method02开始执行')
    # 模拟一个耗时操作,让当前协程挂起,此时其他协程可以执行
    await asyncio.sleep(2)
    print('协程方法method02结束')


# 定义一个主协程,做统一调度
async def main():
    # 创建并发任务
    task01 = asyncio.create_task(method01())
    task02 = asyncio.create_task(method02())

    # 等待所有任务完成,在执行主协程下面的代码
    await task01
    await task02


if __name__ == '__main__':
    # 调用main函数,启动协程
    asyncio.run(main())