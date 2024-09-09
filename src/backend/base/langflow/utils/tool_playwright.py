from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


# 抓取总社新闻，并保存到本地
async def save_page_pdf(url: str, output_pdf_path: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(url)
        await page.wait_for_selector('div.content')

        # 使用 JavaScript 选择并调整指定的 div
        await page.evaluate(f'''
			// 隐藏所有不需要的元素
			document.body.style.margin = '0';
			document.body.style.padding = '0';
			document.body.style.overflow = 'hidden';

			// 选择目标 div，并确保它的内容能分页
			const targetDiv = document.querySelector('div.content');
			if (targetDiv) {{
			    // 删除社交媒体分享
                const divsToRemove = targetDiv.querySelectorAll('div.shareBox');
                divsToRemove.forEach(div => div.remove());

                // 删除字体放大缩小繁体
                const innerDiv = targetDiv.querySelector('div');
                if (innerDiv) {{
                    // 在子 div 中选择第 3 个 <p> 元素并删除
                    const paragraphs = innerDiv.querySelectorAll('p');
                    if (paragraphs.length >= 3) {{
                        paragraphs[2].remove();  // 删除第 3 个 <p> 元素（索引从 0 开始）
                    }}
                }}

			    // 设置目标 div 的样式
                targetDiv.style.border = '0';
                targetDiv.style.padding = '0';
                targetDiv.style.margin = '0'; // 确保没有额外的外边距

				// 克隆目标 div
				const container = document.createElement('div');
				container.style.position = 'absolute';
				container.style.top = '0';
				container.style.left = '0';
				container.style.width = '100vw';
				container.style.height = 'auto';  // 自动高度

				container.style.overflow = 'visible';
				container.appendChild(targetDiv.cloneNode(true));
				document.body.innerHTML = '';
				document.body.appendChild(container);
			}}
		''')

        # 生成 PDF
        await page.pdf(
            path=output_pdf_path,
            format='A5',
            print_background=True,
            margin=dict(top='72px', bottom='72px', left='72px', right='72px')
        )

        await browser.close()


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


# 获取<div class='content'>的文本
async def fetch_webpage_content(url: str):
    html = await fetch_dynamic_content(url)

    # 使用 BeautifulSoup 解析
    soup = BeautifulSoup(html, 'html.parser')
    # 查找指定的 div 标签，class 为 content
    content_div = soup.find('div', class_='content')

    # 提取 div 中的文本内容
    text = ""
    if content_div:
        text = content_div.get_text()  # strip=True 会去掉首尾的空白字符
    else:
        print("未找到指定的 div 元素")
    return text
