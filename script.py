import os
import re
import shutil
from datetime import datetime
from urllib.parse import unquote

# --- 설정값 ---
ORIGIN_DIR = "origin"
POST_DIR = "_posts"
ASSETS_DIR = "assets/images"
AUTHOR_NAME = "jglee"

def sanitize_filename(name):
    """
    파일명으로 사용할 수 없는 문자, 괄호, 특수문자 등을 제거하고
    공백을 하이픈으로 변환하는 강화된 함수.
    """
    # 괄호, 따옴표 등 대부분의 특수문자 제거
    name = re.sub(r'[\\/:"*?<>|()\'"]', '', name).strip()
    # 연속된 공백이나 하이픈을 단일 하이픈으로 변경
    name = re.sub(r'[\s-]+', '-', name)
    return name

def parse_notion_date(date_str):
    """'YYYY/MM/DD' 형식의 날짜를 파싱합니다."""
    if not date_str:
        return datetime.now()
    try:
        return datetime.strptime(date_str.strip(), "%Y/%m/%d")
    except ValueError:
        print(f"⚠️ 알 수 없는 날짜 형식: '{date_str}'. 현재 날짜를 사용합니다.")
        return datetime.now()

def process_post(post_path):
    """개별 포스트 폴더를 처리하여 마크다운 파일을 변환합니다."""
    md_file = next((f for f in os.listdir(post_path) if f.endswith('.md')), None)
    if not md_file:
        print(f"🚫 {os.path.basename(post_path)}에서 마크다운 파일을 찾을 수 없습니다.")
        return

    with open(os.path.join(post_path, md_file), 'r', encoding='utf-8') as f:
        lines = f.readlines()

    metadata = {}
    content_start_index = 0
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if i == 0 and stripped_line.startswith('# '):
            metadata['title'] = stripped_line[2:].strip()
            continue
        
        match = re.match(r'^([\w\s]+):\s*(.*)', stripped_line)
        if match:
            key, value = match.groups()
            if key == '표지': metadata['cover'] = value.strip()
            elif key == 'Tags': metadata['tags'] = [t.strip().lower() for t in value.split(',')]
            elif key == '작성일': metadata['date'] = value.strip()
            elif key == '상태': pass
        elif stripped_line:
            content_start_index = i
            break

    if 'title' not in metadata:
        print(f"🚫 {md_file}에서 제목을 찾을 수 없습니다.")
        return

    title = metadata.get('title')
    created_date = parse_notion_date(metadata.get('date'))
    tags = metadata.get('tags', ['uncategorized'])
    
    post_date_str = created_date.strftime("%Y-%m-%d")
    # 강화된 sanitize_filename 함수 사용
    safe_title = sanitize_filename(title)
    new_post_filename_base = f"{post_date_str}-{safe_title}"
    new_post_filepath = os.path.join(POST_DIR, f"{new_post_filename_base}.md")
    
    image_dir_fs_path = os.path.join(ASSETS_DIR, tags[0], new_post_filename_base)
    os.makedirs(image_dir_fs_path, exist_ok=True)
    image_dir_web_path = image_dir_fs_path.replace("\", "/")
    
    image_location_map = {}
    for root, _, files in os.walk(post_path):
        for name in files:
            if name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                image_location_map[name] = os.path.join(root, name)

    cover_path_final = ""
    if 'cover' in metadata:
        cover_name = os.path.basename(unquote(metadata['cover']))
        if cover_name in image_location_map:
            original_cover_path = image_location_map[cover_name]
            shutil.copy(original_cover_path, os.path.join(image_dir_fs_path, cover_name))
            cover_path_final = os.path.join(image_dir_web_path, cover_name).replace("\\", "/")
        else:
            print(f"⚠️ 커버 이미지 '{cover_name}'을 찾을 수 없습니다.")

    def replace_image_path(match):
        alt, img_path_encoded = match.groups()
        if img_path_encoded.startswith("http"):
            return f"![{alt}]({img_path_encoded})"
        
        img_name = os.path.basename(unquote(img_path_encoded))
        
        if img_name in image_location_map:
            original_img_path = image_location_map[img_name]
            shutil.copy(original_img_path, os.path.join(image_dir_fs_path, img_name))
            new_img_web_path = os.path.join(image_dir_web_path, img_name).replace("\\", "/")
            return f"![{alt}]({new_img_web_path})"
        else:
            print(f"⚠️ 본문 이미지 '{img_name}'을 찾을 수 없습니다.")
            return f"![{alt}]({img_path_encoded})"

    content = "".join(lines[content_start_index:])
    content = re.sub(r"!\[(.*?)\]\((.*?)\)", replace_image_path, content)

    header = f"""---
layout: post
current: post
navigation: True
title: "{title}"
date: {created_date.strftime("%Y-%m-%d 00:00:00")}
cover: "{cover_path_final}"
tags: {tags}
class: post-template
subclass: 'post tag-getting-started'
author: {AUTHOR_NAME}
---
"""
    with open(new_post_filepath, 'w', encoding='utf-8') as f:
        f.write(header + "\n" + content.strip())
    print(f"✅ 성공: '{os.path.basename(new_post_filepath)}' 파일이 생성되었습니다.")

def main():
    """메인 실행 함수"""
    if not os.path.exists(ORIGIN_DIR):
        print(f"'{ORIGIN_DIR}' 폴더를 찾을 수 없습니다. 스크립트와 같은 위치에 만들어주세요.")
        return
        
    os.makedirs(POST_DIR, exist_ok=True)
    
    for item_name in os.listdir(ORIGIN_DIR):
        if item_name.startswith('.'):
            continue
        
        item_path = os.path.join(ORIGIN_DIR, item_name)
        if os.path.isdir(item_path):
            print(f"\n📁 '{item_name}' 폴더 처리를 시작합니다...")
            process_post(item_path)

if __name__ == "__main__":
    main()