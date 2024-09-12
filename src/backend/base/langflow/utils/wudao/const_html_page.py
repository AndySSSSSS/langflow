EXP_GONG_XIAO_NEWS = """
// 隐藏所有不需要的元素
document.body.style.margin = '0';
document.body.style.padding = '0';
document.body.style.overflow = 'hidden';

// 选择目标 div，并确保它的内容能分页
const targetDiv = document.querySelector('div.content');
if (targetDiv) {{
    // 删除字体放大缩小繁体
    const div_source = targetDiv.querySelector('div.source');
    if (div_source) {{
        const paragraphs = div_source.querySelectorAll('p');
        paragraphs[paragraphs.length-1].remove();  // 删除最后1个 <p> 元素（索引从 0 开始）
    }}

    // 删除顶部隐藏的摘要
    const div_abstract = targetDiv.querySelectorAll('div.abstract');
    if (div_abstract) {{
        div_abstract.forEach(div => div.remove());
    }}

    // 删除底部社交媒体分享
    const div_shareBox = targetDiv.querySelectorAll('div.shareBox');
    if (div_shareBox) {{
        div_shareBox.forEach(div => div.remove());
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
"""