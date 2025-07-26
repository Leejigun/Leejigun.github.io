import os

ORIGIN_DIR = "origin"

print(f"--- '{ORIGIN_DIR}' 폴더 검사를 시작합니다. ---")

if not os.path.exists(ORIGIN_DIR):
    print(f"[진단] 스크립트와 같은 위치에 '{ORIGIN_DIR}' 폴더가 없습니다.")
else:
    print(f"[진단] '{ORIGIN_DIR}' 폴더를 찾았습니다.")
    try:
        contents = os.listdir(ORIGIN_DIR)
        if not contents:
            print(" -> 하지만 폴더 안이 비어있습니다. 변환할 포스트의 폴더를 넣어주세요.")
        else:
            print(f" -> 폴더 안의 내용물: {contents}")
            for item_name in contents:
                if item_name.startswith('.'):
                    continue
                item_path = os.path.join(ORIGIN_DIR, item_name)
                if os.path.isdir(item_path):
                    print(f"   - '{item_name}' : 폴더입니다. (O)")
                else:
                    print(f"   - '{item_name}' : 파일입니다. 폴더가 아니므로 처리할 수 없습니다. (X)")
    except Exception as e:
        print(f"폴더 내용을 읽는 중 오류 발생: {e}")

print("--- 검사 종료 ---")