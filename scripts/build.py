#!/usr/bin/env python3
"""Build an offline-friendly, dependency-free weekly journal from Markdown + JSON."""
import datetime as dt
import html
import json
import math
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'site'

def esc(value):
    return html.escape(str(value), quote=True)

def inline(text):
    links = []
    def link(m):
        label, url = m.groups()
        if urlparse(url).scheme not in ('http', 'https'):
            return label
        links.append(f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)}<span class="sr-only">（在新标签页打开）</span></a>')
        return f'\x00LINK{len(links)-1}\x00'
    text = re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)', link, text)
    text = esc(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    for i, value in enumerate(links):
        text = text.replace(f'\x00LINK{i}\x00', value)
    return text

def inline_item(text):
    return inline(re.sub(r"^(\*\*.+?\*\*)[：:]\s*", r"\1 ", text))

def render_md(md):
    """Supported: headings, paragraphs, unordered lists, quotes, pipe tables, links."""
    result, toc = [], []
    for block in re.split(r'\n\s*\n', md.strip()):
        lines = block.splitlines()
        heading = re.fullmatch(r'(#{1,3}) (.+)', lines[0]) if len(lines) == 1 else None
        if heading:
            level, title = len(heading[1]) + 1, heading[2]
            anchor = f'section-{len(toc)+1}'
            toc.append((anchor, title, level))
            result.append(f'<h{level} id="{anchor}" tabindex="-1">{inline(title)}</h{level}>')
        elif re.fullmatch(r'!\[([^\]]+)\]\(([^)]+)\)(?:\n来源：(.+))?', block):
            image = re.fullmatch(r'!\[([^\]]+)\]\(([^)]+)\)(?:\n来源：(.+))?', block)
            alt, src, caption = image.groups()
            parsed = urlparse(src)
            target = (ROOT/'site/issues'/src).resolve()
            if parsed.scheme or parsed.netloc or not target.is_relative_to(OUT.resolve()) or not target.is_file():
                raise ValueError(f'Image must be a local site asset: {src}')
            caption_html = f'<figcaption>{inline(caption)}</figcaption>' if caption else ''
            result.append(f'<figure class="evidence-image"><img src="{esc(src)}" alt="{esc(alt)}" loading="lazy" decoding="async">{caption_html}</figure>')
        elif all(line.startswith('|') for line in lines):
            rows = [[x.strip() for x in line.strip('|').split('|')] for line in lines]
            if len(rows) < 2 or not all(re.fullmatch(r':?-+:?', x) for x in rows[1]):
                raise ValueError('Table requires a Markdown separator row')
            result.append('<div class="table-scroll" tabindex="0" role="region" aria-label="一周速览表"><table><thead><tr>'+''.join(f'<th scope="col">{inline(x)}</th>' for x in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{inline(x)}</td>' for x in row)+'</tr>' for row in rows[2:])+'</tbody></table></div>')
        elif lines[0].startswith('>'):
            quote = ' '.join(re.sub(r'^>\s?', '', line) for line in lines if '[!CALLOUT]' not in line)
            result.append(f'<blockquote>{inline(quote.strip())}</blockquote>')
        elif lines[0].startswith('- '):
            items = re.split(r'\n- ', block[2:])
            result.append('<ul class="story-list">'+''.join(f'<li>{inline_item(x)}</li>' for x in items)+'</ul>')
        else:
            result.append('<p>'+inline(block).replace('\n', '<br>')+'</p>')
    return '\n'.join(result), toc

def header(prefix, active=''):
    return f'''<a class="skip" href="#main">跳到正文</a><header class="site-header"><div class="header-inner">
    <a class="brand" href="{prefix}index.html" aria-label="AI 周报首页"><span class="brand-symbol" aria-hidden="true">◈</span><span>AI WEEKLY<span class="brand-cn"> / 行业周报</span></span></a>
    <nav aria-label="主导航"><a href="{prefix}index.html#archive" {'aria-current="page"' if active == 'archive' else ''}>周报归档</a><a href="{prefix}index.html#about">关于</a><button class="theme-toggle" aria-label="切换到浅色模式" title="切换明暗模式"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.4 1.4m11.2 11.2L19 19M5 19l1.4-1.4M17.6 6.4L19 5"/></svg></button></nav></div></header>'''

def shell(title, body, prefix='', description='每周关注 AI 的实际进展，记录模型、技术与重要观点。'):
    return f'''<!doctype html><html lang="zh-CN" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark light"><meta name="description" content="{esc(description)}"><title>{esc(title)} · AI WEEKLY</title><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><script src="{prefix}assets/theme.js"></script><link rel="stylesheet" href="{prefix}assets/style.css"><script src="{prefix}assets/app.js" defer></script></head><body>{body}<footer class="footer wrap"><a href="{prefix}index.html">AI WEEKLY <span>/ 每周观察</span></a><span>每周一 10:00 开始整理 · Asia/Shanghai</span><a href="#top">回到顶部 ↑</a></footer></body></html>'''

def date_range(item):
    return item['start'].replace('-', '.')+' — '+item['end'][5:].replace('-', '.')

def regions(item, prefix):
    return '<div class="region-grid">'+''.join(f'''<a class="region" href="{prefix}{esc(x['anchor'])}"><span class="eyebrow">{esc(x['label'])}</span><h3>{esc(x['title'])}</h3><p>{esc(x['text'])}</p><span class="region-bottom">{esc(x['region'])}<span aria-hidden="true">↗</span></span></a>''' for x in item['highlights'])+'</div>'

def validate(item, file):
    required = ('slug','title','subtitle','start','end','published','summary','tags','highlights')
    if any(key not in item for key in required):
        raise ValueError(f'{file}: missing required fields')
    dates = [dt.date.fromisoformat(item[x]) for x in ('start','end','published')]
    if dates[0].weekday() != 0 or dates[1].weekday() != 6 or (dates[1]-dates[0]).days != 6 or dates[2] < dates[1]:
        raise ValueError(f'{file}: issue must cover Monday–Sunday')
    if item['slug'] != item['end'] or file.stem != item['slug']:
        raise ValueError(f'{file}: filename and slug must be the ending date')
    if not item['tags'] or len(item['highlights']) != 3:
        raise ValueError(f'{file}: tags and three regional highlights are required')

def journal_stats(issues):
    """Use validated issue metadata for both the website and README."""
    since = min(i['published'] for i in issues).replace('-', '.')
    count = len(issues)
    latest = date_range(issues[0])
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="240" viewBox="0 0 960 240" role="img" aria-labelledby="title desc">
<title id="title">AI Weekly · 周报记录</title><desc id="desc">创刊 {since}，累计 {count} 期，最新一期 {latest}</desc>
<rect width="960" height="240" rx="18" fill="#101b20"/>
<rect x="1" y="1" width="958" height="238" rx="17" fill="none" stroke="#294047"/>
<path d="M32 62H928M330 88V178M630 88V178" stroke="#294047"/>
<circle cx="37" cy="34" r="4" fill="#9ed8c3"/>
<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif">
<text x="52" y="39" fill="#9ed8c3" font-size="13" letter-spacing="2">AI WEEKLY / THE RECORD</text>
<text x="928" y="39" text-anchor="end" fill="#9aafb4" font-size="12">MON · 10:00 · ASIA/SHANGHAI</text>
<g fill="#9aafb4" font-size="14"><text x="36" y="108">创刊日期 / SINCE</text><text x="365" y="108">累计周报 / ISSUES</text><text x="665" y="108">最新一期 / LATEST</text></g>
<text x="36" y="155" fill="#ecf4f3" font-size="32">{since}</text>
<text x="365" y="158" fill="#9ed8c3" font-size="44">{count:03d}<tspan font-size="16" dx="12">期</tspan></text>
<text x="665" y="151" fill="#ecf4f3" font-size="22">{latest}</text>
<text x="36" y="213" fill="#9aafb4" font-size="12">记录每周进展 · 根据仓库内容自动生成</text>
</g></svg>'''
    block = f'''<!-- weekly-stats:start -->
![周报记录：创刊 {since}，累计 {count} 期，最新一期 {latest}](site/assets/weekly-stats.svg)

<sub>创刊日期按首次发布日期计算；统计随每次构建自动更新。</sub>
<!-- weekly-stats:end -->'''
    readme = (ROOT/'README.md').read_text(encoding='utf-8')
    pattern = r'<!-- weekly-stats:start -->.*?<!-- weekly-stats:end -->'
    if len(re.findall(pattern, readme, flags=re.S)) != 1:
        raise ValueError('README must contain exactly one weekly-stats marker pair')
    readme = re.sub(pattern, lambda _: block, readme, flags=re.S)
    return since, count, svg, readme

def build():
    issues = []
    for f in sorted((ROOT/'content/issues').glob('*.json'), reverse=True):
        item = json.loads(f.read_text())
        validate(item, f)
        md = f.with_suffix('.md').read_text()
        prose, toc = render_md(md)
        if len(toc) < 3:
            raise ValueError(f'{f}: missing report sections')
        for highlight in item['highlights']:
            if highlight['anchor'] not in {x[0] for x in toc}:
                raise ValueError(f'{f}: unknown highlight anchor')
        item.update(prose=prose, toc=toc, search_text=' '.join(md.split()), words=len(re.findall(r'[\u4e00-\u9fff]|[A-Za-z]+', md)), source_count=len(set(re.findall(r'https?://[^\s)]+', md))))
        item['minutes'] = max(1, math.ceil(item['words']/400))
        issues.append(item)
    if not issues:
        raise ValueError('No issues found')
    since, count, stats_svg, readme = journal_stats(issues)
    pending = {OUT/'assets/weekly-stats.svg': stats_svg, ROOT/'README.md': readme}
    for index, item in enumerate(issues):
        links = ''.join(f'<a class="toc-level-{level}" href="#{anchor}">{esc(title)}</a>' for anchor,title,level in item['toc'])
        previous = issues[index+1] if index+1 < len(issues) else None
        next_item = issues[index-1] if index > 0 else None
        neighboring = ''.join(f'<a href="{x["slug"]}.html"><span>{label}</span>{esc(x["title"])} →</a>' for label,x in [('上一期',previous),('下一期',next_item)] if x)
        body = header('../')+f'''<div id="top"></div><div class="reading-track" aria-hidden="true"><div id="reading-progress"></div></div><main id="main" class="wrap article-main"><a class="back-link" href="../index.html#archive">← 全部周报</a><div class="article-heading"><p class="eyebrow">ISSUE {len(issues)-index:03d} <span>/</span> {date_range(item)}</p><h1>{esc(item['title'])}</h1><p class="article-subtitle">{esc(item['subtitle'])}</p><div class="article-meta"><span>{esc(item['published'])} 发布</span><span>约 {item['minutes']} 分钟</span><span>{item['source_count']} 个来源</span><button class="print-button" type="button">打印 / 保存 PDF ↗</button></div></div>
        <div class="article-deck"><p>{esc(item['summary'])}</p></div>{regions(item,'#')}
        <div class="reading-layout"><aside class="toc"><p class="eyebrow">本期目录</p><nav aria-label="本期目录">{links}</nav><a class="download" href="../downloads/{item['slug']}.md" download>下载 Markdown ↓</a></aside><article class="prose">{item['prose']}</article></div>
        <div class="article-end"><p class="eyebrow">END OF ISSUE / 本期读毕</p><p>来源链接见正文，可继续查阅原始资料。</p><a class="button secondary" href="../index.html#archive">返回周报归档 ↗</a></div><div class="neighboring">{neighboring}</div></main>'''
        pending[OUT/'issues'/f'{item["slug"]}.html'] = shell(item['title'],body,'../',item['summary'])
        pending[OUT/'downloads'/f'{item["slug"]}.md'] = (ROOT/'content/issues'/f'{item["slug"]}.md').read_text()
    newest = issues[0]
    tags = sorted({tag for i in issues for tag in i['tags']})
    cards = ''.join(f'''<a class="archive-card" href="issues/{i['slug']}.html" data-search="{esc(' '.join([i['title'],i['subtitle'],i['summary'],i['search_text'],*i['tags']]))}" data-tags="{esc(json.dumps(i['tags'],ensure_ascii=False))}"><div class="archive-date"><span>{i['start'][:4]}</span><strong>{i['start'][5:].replace('-','.')}</strong><span>— {i['end'][5:].replace('-','.')}</span></div><div class="archive-content"><div class="tag-row">{''.join('<span>'+esc(t)+'</span>' for t in i['tags'])}</div><h3>{esc(i['title'])}</h3><p>{esc(i['summary'])}</p><span class="archive-meta">{i['minutes']} 分钟阅读 · {i['source_count']} 个来源</span></div><span class="archive-arrow" aria-hidden="true">↗</span></a>''' for i in issues)
    body = header('', 'archive')+f'''<div id="top"></div><main id="main"><section class="intro wrap"><div><p class="eyebrow"><span class="status-dot"></span> A WEEKLY PERSPECTIVE ON AI</p><h1>每周 AI 进展，<br><span>在这里集中阅读。</span></h1><p class="intro-copy">覆盖中美欧厂商、模型与算法、行业观点。<br>每周一更新，附来源链接。</p></div><div class="intro-note"><span class="journal-total"><strong>{count:03d}</strong> 期周报</span><span>创刊于 {since}</span><span class="mono">MON / 10:00</span><span>每周一 · 10:00 开始整理</span><span>中美欧 · 模型 / 算法 / 人物</span></div></section>
    <section class="wrap" aria-labelledby="latest-title"><div class="section-label"><span class="eyebrow">LATEST ISSUE / 最新一期</span><span class="mono">{date_range(newest)}</span></div><div class="feature"><div class="feature-copy"><div class="tag-row">{''.join('<span>'+esc(t)+'</span>' for t in newest['tags'])}</div><h2 id="latest-title">{esc(newest['title'])}</h2><p>{esc(newest['summary'])}</p><div class="feature-actions"><a class="button" href="issues/{newest['slug']}.html">阅读本期 <span>↗</span></a><span class="muted">约 {newest['minutes']} 分钟 · {newest['source_count']} 个来源</span></div></div><div class="feature-art" aria-hidden="true"><div class="orbital orbital-1"></div><div class="orbital orbital-2"></div><div class="orbital orbital-3"></div><div class="orb-core">AI<span>IN MOTION</span></div><span class="orbit-label label-model">MODEL</span><span class="orbit-label label-tool">TOOL</span><span class="orbit-label label-action">ACTION</span><span class="art-footnote">OBSERVE · UNDERSTAND · FOLLOW</span></div></div>{regions(newest,'issues/'+newest['slug']+'.html#')}</section>
    <section class="archive-section wrap" id="archive" aria-labelledby="archive-title"><div class="archive-header"><div><p class="eyebrow">THE ARCHIVE</p><h2 id="archive-title">历期周报</h2></div><span class="archive-count" id="archive-count" aria-live="polite">共 {len(issues)} 期周报</span></div><div class="archive-tools"><label class="search"><span aria-hidden="true">⌕</span><input id="search" type="search" placeholder="搜索模型、厂商或关键词" aria-label="搜索周报"></label><label class="topic-filter"><span class="sr-only">按主题筛选</span><select id="topic"><option value="">全部主题</option>{''.join(f'<option>{esc(t)}</option>' for t in tags)}</select></label></div><div id="archive-list">{cards}</div><div id="empty-state" hidden><h3>没有找到相关周报</h3><p>试试其他关键词，或清除筛选。</p><button class="button secondary" id="clear-search">清除筛选</button></div></section>
    <section class="about wrap" id="about"><div><p class="eyebrow">EDITORIAL NOTES / 阅读说明</p><h2>关注哪些进展，<br>如何整理来源。</h2></div><div class="about-copy"><p>这里记录上一周值得关注的 AI 进展：美国、中国与欧洲的主要厂商，模型与算法的新变化，以及研究者和行业领导者的重要观点。</p><p>优先阅读官方公告、论文、模型卡与当事人原帖；区分厂商自述、独立测评和编辑判断。文章保留来源链接，以及影响结论的测试条件和适用范围。</p><div class="about-meta"><span>每周一 10:00 开始更新</span><span>覆盖前一周一至周日</span></div></div></section></main>'''
    pending[OUT/'index.html'] = shell('AI 行业周报',body)
    for path, data in pending.items():
        path.parent.mkdir(parents=True,exist_ok=True)
        temp = path.with_suffix(path.suffix+'.tmp')
        temp.write_text(data,encoding='utf-8')
        temp.replace(path)
    print(f'Built {len(issues)} issue(s), {len(pending)} files → {OUT}')

if __name__ == '__main__':
    build()
