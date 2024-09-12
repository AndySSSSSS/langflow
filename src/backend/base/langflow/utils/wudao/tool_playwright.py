from datetime import timedelta
from io import BytesIO

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from langflow.utils.wudao.const_html_page import EXP_GONG_XIAO_NEWS
from langflow.utils.wudao.tool_date import normalize_date


async def save_page_pdf(page_url: str, minio_client, bucket_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(page_url)
        await page.wait_for_selector('div.content')

        # 使用 JavaScript 选择并调整指定的 div
        await page.evaluate(EXP_GONG_XIAO_NEWS)

        html = await page.content()
        article = await fetch_webpage_content(html)

        # 生成 PDF
        pdf_bytes = await page.pdf(
            format='A5',
            print_background=True,
            margin=dict(top='72px', bottom='72px', left='72px', right='72px')
        )

        pdf_stream = BytesIO(pdf_bytes)
        filename = article['title'] + '.pdf'
        minio_client.put_object(
            bucket_name,
            filename,
            pdf_stream,
            length=len(pdf_bytes),
            content_type='application/pdf'
        )

        presigned_url = minio_client.presigned_get_object(bucket_name, filename, expires=timedelta(days=7))
        article['presigned_url'] = presigned_url

        await browser.close()
        return article


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
        "time": normalize_date(time),
        "content": content
    }

    return article
