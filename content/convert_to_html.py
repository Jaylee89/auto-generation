#!/usr/bin/env python3
"""
Convert converted.md to HTML with styling.
"""
import markdown
import sys
import os

def convert_markdown_to_html(md_file, html_file):
    """Convert a Markdown file to HTML with custom CSS."""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['extra'])

    # CSS styling
    css = """
    <style>
        body {
            font-family: "PingFang SC", "Microsoft YaHei", "Segoe UI", sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fefefe;
        }
        h1 {
            font-size: 2.2em;
            border-bottom: 2px solid #ddd;
            padding-bottom: 0.3em;
            margin-top: 1.5em;
            margin-bottom: 1em;
        }
        h2 {
            font-size: 1.8em;
            border-bottom: 1px solid #eee;
            padding-bottom: 0.2em;
            margin-top: 1.5em;
            margin-bottom: 0.8em;
        }
        h3 {
            font-size: 1.5em;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
        }
        p {
            margin: 1em 0;
            text-align: justify;
        }
        blockquote {
            border-left: 4px solid #ccc;
            margin: 1.5em 0;
            padding: 0.5em 1em;
            background-color: #f9f9f9;
            color: #555;
            font-style: italic;
        }
        strong {
            font-weight: bold;
            color: #000;
        }
        .keywords {
            font-size: 1.1em;
            margin: 1.5em 0;
            padding: 10px;
            background-color: #f0f8ff;
            border-radius: 5px;
        }
        .author-info {
            font-size: 1em;
            color: #666;
            margin-bottom: 2em;
        }
        .author-info strong {
            color: #444;
        }
        hr {
            border: none;
            border-top: 1px solid #ddd;
            margin: 2em 0;
        }
        @media (max-width: 600px) {
            body {
                padding: 10px;
            }
            h1 { font-size: 1.8em; }
            h2 { font-size: 1.5em; }
            h3 { font-size: 1.3em; }
        }
    </style>
    """

    # Full HTML document
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{os.path.basename(md_file)} - HTML 转换</title>
    {css}
</head>
<body>
    {html_content}
</body>
</html>
"""

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"转换完成: {html_file}")

if __name__ == '__main__':
    md_file = 'converted.md'
    html_file = 'converted.html'
    if len(sys.argv) > 1:
        md_file = sys.argv[1]
    if len(sys.argv) > 2:
        html_file = sys.argv[2]
    convert_markdown_to_html(md_file, html_file)