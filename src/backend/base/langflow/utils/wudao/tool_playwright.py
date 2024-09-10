import os

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from langflow.utils.wudao.const_html_page import EXP_GONG_XIAO_NEWS


async def save_page_pdf(page_url: str, save_pdf_path: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(page_url)
        await page.wait_for_selector('div.content')

        # 使用 JavaScript 选择并调整指定的 div
        await page.evaluate(EXP_GONG_XIAO_NEWS)

        html = await page.content()
        article = await fetch_webpage_content(html)

        if not save_pdf_path.endswith(os.sep):
            save_pdf_path = save_pdf_path + os.sep
        save_pdf_path = save_pdf_path + article['title'] + '.pdf'

        # 生成 PDF
        await page.pdf(
            path=save_pdf_path,
            format='A5',
            print_background=True,
            margin=dict(top='72px', bottom='72px', left='72px', right='72px')
        )

        await browser.close()
        return article


# 使用 Playwright 获取动态渲染后的 HTML
async def fetch_dynamic_content(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # 无头模式
        page = await browser.new_page()
        await page.goto(url)

        # # 等待页面加载，可以根据需要调整时间
        # await page.wait_for_timeout(3000)  # 等待 3 秒
        # 等待指定的 div 元素出现 (等待 class 为 content 的 div)
        await page.wait_for_selector('div.content')

        # 获取动态渲染后的 HTML
        html = await page.content()
        await browser.close()
        return html


async def fetch_webpage_content(html: str):
    soup = BeautifulSoup(html, 'html.parser')

    # 标题
    title = ""
    div_title = soup.find('div', class_='titleMess')
    if div_title:
        t = div_title.find('h4')
        if t:
            title = t.get_text()
    if len(title) == 0:
        title = div_title.get_text()

    # 时间
    time = ""
    div_source = soup.find('div', class_='source')
    if div_source:
        times = div_source.find_all('p')
        if times:
            t = times[len(times) - 1]
            if t.get_text() and "发布时间：" in t.get_text():
                time = t.get_text().split("发布时间：")[1]

    # 内容
    content = ""
    div_content = soup.find('div', class_='centerText')
    if div_content:
        content = div_content.get_text()

    article = {
        "title": title,
        "time": time,
        "content": content
    }

    return article
