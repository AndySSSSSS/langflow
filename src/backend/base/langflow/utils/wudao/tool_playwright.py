from datetime import timedelta
from io import BytesIO
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup

from langflow.base.logger.index import AsyncLogger
from langflow.utils.wudao.const_html_page import EXP_GONG_XIAO_NEWS
from langflow.utils.wudao.tool_date import normalize_date
from playwright.async_api import async_playwright


async def loop_for_page(page, count):
    await page.reload()
    await page.wait_for_selector('div.content')
    await page.evaluate(EXP_GONG_XIAO_NEWS)
    html = await page.content()
    article = await fetch_webpage_content(html)
    if count > 0 and len(article['title']) == 0:
        AsyncLogger.log(f'5s后尝试重新获取页面，剩余次数：{str(count - 1)}')
        await page.wait_for_timeout(5000)
        article = await loop_for_page(page, count - 1)
    return article


async def save_page_pdf(page_url: str, minio_client, bucket_name) -> dict:
    async with async_playwright() as p:
        try:
            if page_url is None or 'news.html' not in page_url:
                return {'error': '网址无效'}

            browser = await p.chromium.launch()
            page = await browser.new_page()
            # 设置请求头，告诉服务器接受 UTF-8 编码
            await page.set_extra_http_headers({
                'Accept-Language': 'zh-CN,zh;q=0.9'
            })

            await page.goto(page_url)
            await page.wait_for_timeout(3000)

            article = await loop_for_page(page, 5)

            if len(article['title']) == 0:
                return {'error': '页面获取失败'}

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
            article['aid'] = get_url_param(page_url, 'aid')

            await browser.close()
            AsyncLogger.log(f"Saving page success：[{page_url}] to MinIO bucket: [{bucket_name}]")
            return article
        except Exception as e:
            AsyncLogger.log(f'save_page_pdf error: {e}')
            return {'error': '获取页面失败'}


def get_full_url(url: str) -> str:
    if url.startswith("./"):
        return f'https://www.chinacoop.gov.cn/{url[2:]}'
    else:
        return url


def get_url_param(url: str, param: str) -> str or None:
    # 解析 URL
    parsed_url = urlparse(url)
    # 获取查询参数
    query_params = parse_qs(parsed_url.query)
    # 获取 id 参数的值
    id_value = query_params.get(param)
    if id_value is None:
        return None
    else:
        return id_value[0]


async def get_article_column(html: str) -> dict:
    article_column = {
        'column_id': '',
        'column_link': '',
        'column_type': '',
    }
    soup = BeautifulSoup(html, 'html.parser')
    div_location = soup.find('div', class_='locationBox')
    links = div_location.find_all('a')

    for link in links:
        if link.has_attr('href') and 'column.html' in link['href']:
            article_column['column_type'] = link.get_text()
            article_column['column_link'] = get_full_url(link['href'])
            article_column['column_id'] = get_url_param(link['href'], 'id')
    return article_column


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
        title = div_title.get_text(strip=True)

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
