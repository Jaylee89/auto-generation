import re

def convert_to_markdown(text):
    lines = text.split('\n')
    output = []
    in_abstract = False
    in_keywords = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        # 标题检测
        if i == 0 and stripped:
            output.append(f'# {stripped}\n')
            continue
        # 作者行
        if i == 2 and stripped:
            output.append(f'**作者**: {stripped}\n')
            continue
        # 机构行
        if i == 3 and stripped:
            output.append(f'**机构**: {stripped}\n')
            continue
        # 摘要
        if stripped.startswith('【摘要】'):
            content = stripped[4:].strip()
            output.append('## 摘要\n')
            output.append(f'> {content}\n')
            in_abstract = True
            continue
        # 关键词
        if stripped.startswith('【关键词】'):
            content = stripped[5:].strip()
            output.append('## 关键词\n')
            # 用粗体强调
            keywords = content.split('；')
            formatted = '；'.join([f'**{k.strip()}**' for k in keywords if k.strip()])
            output.append(f'{formatted}\n')
            in_keywords = True
            continue
        # 章节标题：一、二、三...
        if re.match(r'^[一二三四五六七八九十]+、', stripped):
            # 去除数字后的顿号
            title = re.sub(r'^[一二三四五六七八九十]+、', '', stripped)
            output.append(f'## {title}\n')
            continue
        # 子标题（如1. 2.）但原文没有，跳过
        # 普通段落
        if stripped:
            # 加粗炎症性肠病、克罗恩病等关键词
            para = stripped
            para = re.sub(r'炎症性肠病', '**炎症性肠病**', para)
            para = re.sub(r'克罗恩病', '**克罗恩病**', para)
            para = re.sub(r'溃疡性结肠炎', '**溃疡性结肠炎**', para)
            para = re.sub(r'EN', '**EN**', para)
            para = re.sub(r'EEN', '**EEN**', para)
            para = re.sub(r'PEN', '**PEN**', para)
            output.append(para + '\n\n')
        else:
            # 空行
            if output and output[-1] != '\n':
                output.append('\n')
    return ''.join(output)

def main():
    with open('data.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    markdown = convert_to_markdown(text)
    with open('converted.md', 'w', encoding='utf-8') as f:
        f.write(markdown)
    print('转换完成，输出到 converted.md')

if __name__ == '__main__':
    main()