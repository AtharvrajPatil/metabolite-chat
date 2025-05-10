import os
import aiohttp
import asyncio
from aiohttp import ClientError
from tqdm import tqdm

# 定义保存文件夹
target_folder = "test_crawl"
os.makedirs(target_folder, exist_ok=True)

# 定义网页列表
webs = ["https://hmdb.ca/metabolites/HMDB0000001", "https://hmdb.ca/metabolites/HMDB0000030"]  # 填入你的网页列表

# 下载单个网页
# 定义信号量，用于限制并发数量
CONCURRENT_REQUESTS = 10  # 最大并发数
semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
failed_urls = []

# 下载单个网页
async def download_page(session, url, target_path, retries=5, backoff_factor=2):
    async with semaphore:  # 限制并发
        for attempt in range(retries):
            try:
                async with session.get(url, timeout=20) as response:
                    if response.status == 200:
                        content = await response.text()
                        with open(target_path, "w", encoding="utf-8") as file:
                            file.write(content)
                        return True
                    elif response.status == 503:
                        await asyncio.sleep(backoff_factor ** attempt)
                    else:
                        return url
            except ClientError:
                await asyncio.sleep(backoff_factor ** attempt)
        return url

# 异步主函数
async def main_async():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(webs):
            filename = f"{url.split('/')[-1]}.html"
            target_path = os.path.join(target_folder, filename)
            if os.path.exists(target_path):
                continue  # 跳过已存在的文件
            tasks.append(download_page(session, url, target_path))

        # 使用 tqdm 显示进度条
        for future in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Downloading"):
            if isinstance(future, str):
                print("Failed to download a page.")
                failed_urls.append(url)

        # 将失败的URL记录到文件
        if failed_urls:
            failed_log_path = os.path.join(target_folder, "failed_urls.txt")
            with open(failed_log_path, "w", encoding="utf-8") as log_file:
                log_file.write("\n".join(failed_urls))
            print(f"Failed URLs have been saved to {failed_log_path}")


if __name__ == "__main__":
    asyncio.run(main_async())
