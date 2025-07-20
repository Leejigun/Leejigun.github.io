
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
    # "YYYY/MM/DD" 또는 "YYYY/MM/DD 시간..." 형식 처리
    try:
        date_part = date_str.split(' ')[0]
        return datetime.strptime(date_part, "%Y/%m/%d")
    except (ValueError, IndexError):
        pass

    # "YYYY년 MM월 DD일..." 형식 처리
    try:
        # "오전/오후" 및 시간 부분을 제거
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
    last_metadata_line_index = -1

    # 메타데이터 파싱 및 마지막 메타데이터 라인 인덱스 찾기
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith('# '):
            if not title: # 첫 번째 제목만 파싱
                title = stripped_line.strip('# ').strip()
            last_metadata_line_index = i
        elif stripped_line.startswith('작성일:'):
            created_date_str = stripped_line.strip('작성일:').strip()
            last_metadata_line_index = i
        elif stripped_line.startswith('Tags:'):
            tags = [t.strip().lower() for t in stripped_line.strip('Tags:').split(',')]
            last_metadata_line_index = i
        elif stripped_line.startswith('표지:'):
            cover_image_str = stripped_line.strip('표지:').strip()
            last_metadata_line_index = i
        elif any(stripped_line.startswith(key) for key in ['URL:', '상태:']):
            last_metadata_line_index = i

    if not title:
        print(f"{md_file}에서 제목을 찾을 수 없습니다. 건너뜁니다.")
        return

    # 마지막 메타데이터 라인 이후부터 본문 추출
    content_lines = []
    if last_metadata_line_index != -1:
        # 메타데이터 바로 다음 줄부터 시작하되, 앞부분의 공백 라인은 제거
        content_started = False
        for i in range(last_metadata_line_index + 1, len(lines)):
            if not content_started and lines[i].strip() == "":
                continue # 본문 시작 전의 공백 라인 건너뛰기
            content_started = True
            content_lines.append(lines[i])

    content = "".join(content_lines)
    created_date = parse_notion_date(created_date_str) if created_date_str else datetime.now()
    tags = tags if tags else ['uncategorized']

    post_date_str = created_date.strftime("%Y-%m-%d")
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-')
    new_post_filename_base = f"{post_date_str}-{safe_title}"
    new_post_filepath = os.path.join(POST_DIR, f"{new_post_filename_base}.md")

    image_base_path = f"assets/images/{tags[0]}/{new_post_filename_base}"
    os.makedirs(image_base_path, exist_ok=True)

    # finditer를 사용하여 모든 이미지 링크를 명시적으로 순회하고 처리
    new_content = content
    # finditer는 이터레이터를 반환하므로 리스트로 변환하여 사용
    matches = list(re.finditer(r"!\[(.*?)\]\((.*?)\)", content))
    # 역순으로 처리해야 교체 시 인덱스가 꼬이지 않음
    for match in reversed(matches):
        alt, img_path = match.groups()
        if img_path.startswith("http"):
            continue

        # 마크다운 파일 위치를 기준으로 상대 경로 조합 (가장 안정적인 방법)
        original_fs_path = os.path.join(post_path, unquote(img_path))
        img_name = os.path.basename(unquote(img_path))
        new_web_path = f"{image_base_path}/{img_name}"
        new_fs_path = os.path.join(image_base_path, img_name)

        if os.path.exists(original_fs_path):
            shutil.copy(original_fs_path, new_fs_path)
        else:
            print(f"이미지 파일을 찾을 수 없습니다: {original_fs_path}")
            continue

        # 원본 문자열에서 현재 일치 항목을 새 이미지 경로로 교체
        start, end = match.span()
        new_content = new_content[:start] + f"![{alt}]({new_web_path})" + new_content[end:]

    content = new_content
    
    cover_path = ""
    if cover_image_str:
        # 마크다운 파일 위치를 기준으로 상대 경로 조합 (가장 안정적인 방법)
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

    # 재귀적으로 origin 폴더를 탐색하여 md 파일이 있는 폴더를 찾음
    for root, dirs, files in os.walk(ORIGIN_DIR):
        # .DS_Store 같은 숨김 파일/폴더는 건너뜀
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        if any(f.endswith('.md') for f in files):
            post_folder_path = root
            print(f"'{post_folder_path}' 폴더 처리를 시작합니다...")
            try:
                process_post(post_folder_path)
                # 처리된 폴더를 archive로 이동 (최상위 폴더 기준)
                top_level_folder = os.path.join(ORIGIN_DIR, post_folder_path.split(os.path.sep)[1])
                if os.path.exists(top_level_folder):
                     shutil.move(top_level_folder, os.path.join(ARCHIVE_DIR, os.path.basename(top_level_folder)))
                     print(f"'{os.path.basename(top_level_folder)}' 폴더를 '{ARCHIVE_DIR}'로 이동했습니다.")
            except Exception as e:
                print(f"'{post_folder_path}' 처리 중 오류 발생: {e}")
            # 한 번에 하나의 포스트만 처리한다고 가정하고 루프 종료
            break

if __name__ == "__main__":
    main()
