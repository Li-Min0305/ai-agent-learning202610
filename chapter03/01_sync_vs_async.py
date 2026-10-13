import time
import asyncio


def sync_task(user_id : int):
    print(f"[同步]正在处理用户 {user_id} 的请求...")
    time.sleep(2)
    print(f"[同步]用户 {user_id} 的回答生成完毕")

def run_sync():
    print("开始模拟3个用户同时提问")
    start_time = time.time()

    for i in range(1, 4):
        sync_task(i)

    print(f"总耗时：{time.time() - start_time:.2f} 秒\n")

async def async_task(user_id : int):
    print(f"[异步]正在处理用户 {user_id} 的请求...")
    await asyncio.sleep(2)
    print(f"  [异步] 用户 {user_id} 的回答生成完毕！")

async def run_async():
    print("模拟3个用户提问（异步")
    start_time = time.time()

    await asyncio.gather(
        async_task(1),
        async_task(2),
        async_task(3)
    )

    print(f"总耗时：{time.time() - start_time:.2f} 秒\n")

if __name__ == "__main__":
    run_sync()
    asyncio.run(run_async())