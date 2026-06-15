#HTML
import re

def extract_html_links(html_content):
    """
    从HTML字符串中提取所有<a>标签的href和文本
    """
    # 匹配 <a href="...">文本</a>
    link_pattern = r'<a\s+(?:[^>]*?\s+)?href=["\']([^"\']*)["\'][^>]*>(.*?)</a>'
    
    links = re.findall(link_pattern, html_content, re.DOTALL | re.IGNORECASE)
    
    # 清理提取的文本（去除HTML标签和多余空白）
    cleaned_links = []
    for href, text in links:
        # 去除文本中的HTML标签
        clean_text = re.sub(r'<[^>]+>', '', text)
        # 去除多余空白
        clean_text = ' '.join(clean_text.split())
        cleaned_links.append({
            'href': href,
            'text': clean_text
        })
    
    # 输出结果
    print("=" * 60)
    print("🔗 HTML链接提取结果")
    print("=" * 60)
    print(f"共找到 {len(cleaned_links)} 个链接：\n")
    
    for i, link in enumerate(cleaned_links, 1):
        print(f"{i}. 📎 {link['text']}")
        print(f"   🔗 {link['href']}")
        print()
    
    print("=" * 60)
    
    return cleaned_links

def extract_links_advanced(html_content):
    """
    更强大的链接提取器（处理更多情况）
    """
    # 匹配各种引号和属性顺序
    pattern = r'<a\s+([^>]+)>(.*?)</a\s*>'
    matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
    
    links = []
    for attrs, text in matches:
        # 提取href属性
        href_match = re.search(r'href\s*=\s*["\']([^"\']*)["\']', attrs, re.IGNORECASE)
        href = href_match.group(1) if href_match else ''
        
        # 清理文本
        clean_text = re.sub(r'<[^>]+>', '', text)
        clean_text = ' '.join(clean_text.split())
        
        # 提取其他属性（如title, class等）
        title_match = re.search(r'title\s*=\s*["\']([^"\']*)["\']', attrs, re.IGNORECASE)
        title = title_match.group(1) if title_match else ''
        
        links.append({
            'href': href,
            'text': clean_text,
            'title': title,
            'attributes': attrs
        })
    
    return links

# 测试HTML
test_html = """
<!DOCTYPE html>
<html>
<head>
    <title>测试页面</title>
</head>
<body>
    <h1>欢迎访问我们的网站</h1>
    
    <nav>
        <a href="https://www.example.com">首页</a>
        <a href="https://www.example.com/about">关于我们</a>
        <a href="https://www.example.com/products">产品展示</a>
        <a href="https://www.example.com/contact" title="联系我们">联系方式</a>
    </nav>
    
    <div class="content">
        <p>更多资源：</p>
        <ul>
            <li><a href="/docs/guide.pdf">用户指南 (PDF)</a></li>
            <li><a href="https://github.com/example" class="external">GitHub仓库</a></li>
            <li><a href='https://blog.example.com'>技术博客</a></li>
        </ul>
    </div>
    
    <footer>
        <a href="/privacy">隐私政策</a> | 
        <a href="/terms">服务条款</a>
    </footer>
</body>
</html>
"""

# 运行提取
links = extract_html_links(test_html)