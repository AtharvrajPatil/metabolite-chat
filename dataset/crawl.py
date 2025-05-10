import os
import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from tqdm import trange
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.asyncio import tqdm
import json


def process_one_html(page_content):
    # 解析 HTML
    soup = BeautifulSoup(page_content, 'html.parser')

    target_rows = soup.find_all('tr')
    target = None
    for i in range(len(target_rows)):
        row = target_rows[i]
        if 'Experimental Chromatographic Properties' in row.contents[0].text:
            target = row

    if target is None:
        return "none"

    temp_list = []
    table_rows = target.find_all('tr')
    if len(table_rows) < 2:
        return "none"
    for row in table_rows:
        # 获取每行的单元格内容
        cells = row.find_all(['th', 'td'])
        temp_list.append([cell.text.strip() for cell in cells])
    result = []
    keys = temp_list[0]
    for i in range(1, len(temp_list)):
        tmp_dict = {}
        for j in range(len(keys)):
            key = keys[j]
            tmp_dict[key] = temp_list[i][j]
        result.append(tmp_dict)
    return result


def test_one():
    # 示例 URL（替换为实际网页地址）
    url = "https://hmdb.ca/metabolites/HMDB0000001"
    # url = "https://hmdb.ca/metabolites/HMDB0194346"
    # 获取网页内容
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"请求失败，状态码：{response.status_code}")
        exit()

    print(process_one_html(page_content=html_content))


# 异步爬取函数
async def fetch_page(session, url, semaphore, retries=3, delay=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
    }
    async with semaphore:
        for attempt in range(retries):
            try:
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        return await response.text()
                    elif response.status == 503:
                        # print(f"503 错误，重试第 {attempt + 1} 次：{url}")
                        await asyncio.sleep(delay)
                    else:
                        # print(f"爬取失败 {url}，状态码：{response.status}")
                        return None
            except Exception as e:
                # print(f"爬取 {url} 时出错：{e}")
                await asyncio.sleep(delay)
        # print(f"多次重试后仍然失败：{url}")
        return None


async def fetch_and_process(webs, max_concurrent_tasks=10):
    semaphore = asyncio.Semaphore(max_concurrent_tasks)
    error_sites = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url, semaphore) for url in webs]
        results = [None] * len(webs)

        for idx, task in tqdm(enumerate(asyncio.as_completed(tasks)), total=len(tasks)):
            try:
                html = await task
                if html is None:
                    error_sites.append(webs[idx])
                    print(len(error_sites))
                    continue
                results[idx] = process_one_html(html)
            except Exception as e:
                # print(f"任务 {idx} 出现异常：{e}")
                error_sites.append(webs[idx])

        return results, error_sites


# 主函数
async def main(webs):
    max_concurrent_tasks = 10  # 限制最大并发任务数
    # webs = ["https://hmdb.ca/metabolites/HMDB0000030", "https://hmdb.ca/metabolites/HMDB0000001"]
    results, error_sites = await fetch_and_process(webs, max_concurrent_tasks)
    print(f"处理完成，成功处理 {len([r for r in results if r])} 个网页。")
    return results, error_sites


def crawl():
    origin_data_path = "metabolites_detail_full.json"
    r = open(origin_data_path, "r", encoding="utf-8")
    origin_data = json.load(r)
    r.close()

    keys = list(origin_data.keys())
    keys_length = len(keys)
    keys = keys[int(0.5 * keys_length):]
    # r = open("error_websites.txt", "r", encoding="utf-8")
    # error_websites = r.readlines()
    # r.close()
    # keys = [web.split('/')[-1] for web in error_websites]
    # webs = [f"https://hmdb.ca/metabolites/{key}" for key in keys]
    webs = ["https://hmdb.ca/metabolites/HMDB0000001", "https://hmdb.ca/metabolites/HMDB0000030"]
    # 运行主函数
    results, error_sites = asyncio.run(main(webs))
    with open("error_websites_1.txt", "w", encoding="utf-8") as w:
        for site in error_sites:
            w.write(site)
            w.write('\n')
    for i in range(len(keys)):
        key = keys[i]
        origin_data[key]['experimental_chromatographic_properties'] = results[i]
    with open("metabolites_detail_full.json", "w", encoding="utf-8") as w:
        json.dump(origin_data, w, indent=2, ensure_ascii=False)


def one_by_one():
    origin_data_path = "metabolites_detail.json"
    r = open(origin_data_path, "r", encoding="utf-8")
    origin_data = json.load(r)
    r.close()

    keys = list(origin_data.keys())
    keys_length = len(keys)
    # keys = keys[int(0.5 * keys_length):]
    # r = open("error_websites.txt", "r", encoding="utf-8")
    # error_websites = r.readlines()
    # r.close()
    # keys = [web.split('/')[-1] for web in error_websites]
    webs = [f"https://hmdb.ca/metabolites/{key}" for key in keys]
    # webs = ["https://hmdb.ca/metabolites/HMDB0000001", "https://hmdb.ca/metabolites/HMDB0000030"]
    # 运行主函数
    results = []
    error_sites = []
    for i in trange(len(webs)):
        web = webs[i]
        response = requests.get(web)
        html_content = "none"
        if response.status_code == 200:
            html_content = response.text
        else:
            error_sites.append(web)
            print(len(error_sites))
        results.append(process_one_html(html_content))

    with open("error_websites.txt", "w", encoding="utf-8") as w:
        for site in error_sites:
            w.write(site)
            w.write('\n')
    for i in range(len(keys)):
        key = keys[i]
        origin_data[key]['experimental_chromatographic_properties'] = results[i]
    with open("metabolites_detail_full.json", "w", encoding="utf-8") as w:
        json.dump(origin_data, w, indent=2, ensure_ascii=False)


def local_crawl():
    origin_data_path = "metabolites_detail.json"
    html_path = "/data2/Dingcheng/datasets/metabolite/html"
    r = open(origin_data_path, "r", encoding="utf-8")
    origin_data = json.load(r)
    r.close()

    keys = list(origin_data.keys())
    keys_length = len(keys)

    for i in range(keys_length):
        key = keys[i]
        file_path = os.path.join(html_path, f"{key}.html")
        r = open(file_path, "r", encoding="utf-8")
        html_content = r.read()
        result = process_one_html(html_content)
        origin_data[key]['experimental_chromatographic_properties'] = result
        r.close()

    with open("metabolites_detail_full.json", "w", encoding="utf-8") as w:
        json.dump(origin_data, w, indent=2, ensure_ascii=False)


def process_one_file(file_path):
    if not os.path.exists(file_path):
        return "none"
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return process_one_html(html_content)


def crawl_local_multithreaded():
    origin_data_path = "metabolites_detail.json"
    html_path = "/data2/Dingcheng/datasets/metabolite/html"
    r = open(origin_data_path, "r", encoding="utf-8")
    origin_data = json.load(r)
    r.close()

    keys = list(origin_data.keys())
    file_list = [os.path.join(html_path, f"{key}.html") for key in keys]

    with ThreadPoolExecutor() as executor:
        # 提交任务
        future_to_file = {executor.submit(process_one_file, file): file for file in file_list}

        # 使用 tqdm 显示进度条
        for future in tqdm(as_completed(future_to_file), total=len(file_list), desc="Reading files"):
            file_name = future_to_file[future]
            file_name = file_name.split('/')[-1]
            file_name = file_name.split('.')[0]
            origin_data[file_name]['experimental_chromatographic_properties'] = future.result()

    with open("metabolites_detail_full.json", "w", encoding="utf-8") as w:
        json.dump(origin_data, w, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # test_one()
    # crawl()
    one_by_one()
