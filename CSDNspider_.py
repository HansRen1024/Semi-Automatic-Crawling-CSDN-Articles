"""
 - 去CSDN把需要爬取的文章地址粘贴复制到csdn_url.txt中,一行一个地址;
 - 文章题目如果有/,会被删除掉;
 - 如果是想把文章放到github page上, 可以放开42, 44行.
"""
import requests, os, gne, html2text, kuser_agent
from bs4 import BeautifulSoup
from tqdm import tqdm

with open('./csdn_url.txt', 'r') as f:
    urls = f.readlines()

bar = tqdm(urls)
for url in bar:
    url = url.strip()
    # 1. 获取整个页面数据
    html = requests.get(url=url,headers={'User-Agent':kuser_agent.get()}).content

    # 2.提取关键内容
    extractor = gne.GeneralNewsExtractor()
    keyinfo = extractor.extract(requests.get(url=url,headers={'User-Agent':kuser_agent.get()}).text)
    title = keyinfo["title"].replace("/", "")
    date = keyinfo["publish_time"].split(" ")[0]
    file_name = f'{date}-{title}.md' 
    bar.set_postfix(name=file_name)

    # 3. 提取正文中的HTML文本
    bs = BeautifulSoup(html, features="lxml")
    text = bs.find(attrs={'id':'article_content'}).prettify()

    # 4. 将HTML文本转成Markdown格式
    ht = html2text.HTML2Text()
    ht.bypass_tables = False
    ht.mark_code = True
    ht.code = True
    result = ht.handle(text)
    delets = ["[code]", "[/code]"]
    for info in delets:
        result = result.replace(info, '')

    # 5. 保存内容到本地
    # head = f"---\ntitle: '{title}'\ndate: {date}\npermalink: /posts/{date.split('-')[0]}/{date.split('-')[1]}/{title}/\n---\n\n---\n\n"
    with open(file_name, 'w') as f:
        # f.write(head)
        f.write(result.strip())
bar.close()