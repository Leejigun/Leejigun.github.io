
import os
import re
import shutil
from datetime import datetime
from urllib.parse import unquote

ORIGIN_DIR = "origin"
POST_DIR = "_posts"
ARCHIVE_DIR = "archive"

def parse_notion_date(date_str):
    date_str = date_str.strip()
    if re.match(r"^\d{4}/\d{1,2}/\d{1,2}$", date_str):
        return datetime.strptime(date_str, "%Y/%m/%d")
    try:
        date_part = re.sub(r"\s+(오전|오후)\s+\d{1,2}:\d{1,2}", "", date_str).strip()
        return datetime.strptime(date_part, "%Y년 %m월 %d일")
    except ValueError:
        pass
    print(f"알 수 없는 날짜 형식: '{date_str}'. 현재 날짜를 사용합니다.")
    return datetime.now()

def process_post(post_path):
    md_file = next((f for f in os.listdir(post_path) if f.endswith('.md')), None)
    if not md_file:
        print(f"{post_path}에서 마크다운 파일을 찾을 수 없습니다.")
        return

    with open(os.path.join(post_path, md_file), 'r', encoding='utf-8') as f:
        lines = f.readlines()

    title, created_date_str, tags, cover_image_str = "", "", [], ""
    content_lines = []
    header_ended = False

    for line in lines:
        if not header_ended:
            if line.strip().startswith('# '):
                title = line.strip('# ').strip()
            elif line.strip().startswith('작성일:'):
                created_date_str = line.strip('작성일:').strip()
            elif line.strip().startswith('Tags:'):
                tags = [t.strip().lower() for t in line.strip('Tags:').split(',')]
            elif line.strip().startswith('표지:'):
                cover_image_str = line.strip('표지:').strip()
            elif line.strip() == '---':
                header_ended = True
        else:
            content_lines.append(line)

    if not content_lines:
        content_started = False
        for line in lines:
            if content_started:
                content_lines.append(line)
            elif line.strip().startswith('# '):
                content_started = True
                content_lines.append(line)

    if not title:
        print(f"{md_file}에서 제목을 찾을 수 없습니다. 건너뜁니다.")
        return

    content = "".join(content_lines)
    created_date = parse_notion_date(created_date_str) if created_date_str else datetime.now()
    tags = tags if tags else ['uncategorized']

    post_date_str = created_date.strftime("%Y-%m-%d")
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-')
    new_post_filename_base = f"{post_date_str}-{safe_title}"
    new_post_filepath = os.path.join(POST_DIR, f"{new_post_filename_base}.md")

    image_base_path = f"assets/images/{tags[0]}/{new_post_filename_base}"
    os.makedirs(image_base_path, exist_ok=True)

    def replace_image_path(match):
        alt, img_path = match.groups()
        if img_path.startswith("http"):
            return f"![{alt}]({img_path})"
        
        original_fs_path = os.path.join(post_path, unquote(img_path))
        img_name = os.path.basename(unquote(img_path))
        new_web_path = f"{image_base_path}/{img_name}"
        new_fs_path = os.path.join(image_base_path, img_name)

        if os.path.exists(original_fs_path):
            shutil.copy(original_fs_path, new_fs_path)
        else:
            print(f"이미지 파일을 찾을 수 없습니다: {original_fs_path}")
        
        return f"![{alt}]({new_web_path})"

    content = re.sub(r"!\[(.*?)\]\((.*?)\)", replace_image_path, content)
    
    cover_path = ""
    if cover_image_str:
        original_cover_path = os.path.join(post_path, unquote(cover_image_str))
        cover_name = os.path.basename(unquote(cover_image_str))
        cover_path = f"{image_base_path}/{cover_name}"
        new_cover_fs_path = os.path.join(image_base_path, cover_name)
        if os.path.exists(original_cover_path):
            shutil.copy(original_cover_path, new_cover_fs_path)

    header = f"""---
layout: post
current: post
navigation: True
title: "{title}"
date: {created_date.strftime("%Y-%m-%d %H:%M:%S")}
cover: {cover_path}
tags: {tags}
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
"""
    with open(new_post_filepath, 'w', encoding='utf-8') as f:
        f.write(header + content)
    print(f"성공적으로 처리되었습니다: {new_post_filename_base}.md")

def main():
    if not os.path.exists(ORIGIN_DIR):
        print(f"'{ORIGIN_DIR}' 폴더를 찾을 수 없습니다.")
        return
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    for folder_name in os.listdir(ORIGIN_DIR):
        folder_path = os.path.join(ORIGIN_DIR, folder_name)
        if os.path.isdir(folder_path):
            print(f"'{folder_name}' 폴더 처리를 시작합니다...")
            try:
                process_post(folder_path)
                shutil.move(folder_path, os.path.join(ARCHIVE_DIR, folder_name))
                print(f"'{folder_name}' 폴더를 '{ARCHIVE_DIR}'로 이동했습니다.")
            except Exception as e:
                print(f"'{folder_name}' 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
