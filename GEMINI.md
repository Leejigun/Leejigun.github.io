
# 개요
해당 깃 레포지토리는 git blog 를 위한 레포지토리이다.
빌드 후 output 서브모듈을 배포하면 https://leejigun.github.io 에 반영된다.

# 규칙
나는 8년차 iOS 개발자로 iOS, Swift, Clean Archtecture, Flutter, Dart에 관심이 많다.
해당 블로그는 주로 그와 관련된 내용을 배포하며, 나는 노션에 마크타운으로 먼저 글을 작성하고, 다운받아 이 프로젝트에 넣어서 배포하고 있다.

블로그 글은 항상 _posts 폴더에 있고, 작성날짜-제목.md 파일 형태를 가지고 있다. (ex: 2023-07-20-CleanSoftware_SRP)
블로그 해더 부분에는 해당 블로그의 정보가 저장되어 있다.
예시: 
---
layout: post
current: post
navigation: True
title:  "[클린 소프트웨어] 단일책임원칙(SRP)"
date:   2023-07-20 00:00:02
cover: assets/images/CS/clean_software/2023-07-20-CleanSoftware_SRP/images.png
description: "[클린 소프트웨어] 단일책임원칙(SRP)"
tags: [ cs ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

이미지의 경우 assets/images/{태그이름}/대분류/제목/{이미지이름}.{확장자} 형태를 띄고 있다.
다만 노션에서 다운받은 이미지의 경로가 다르기 때문에 경로를 위와 같은 형태로 변경해줘야 한다.

태그의 경우 _data/tags.yml 파일에 정의되어 있는 태그 소문자로 사용하고 있다.

# 원하는 것
내가 원하는 것은 지금까지는 노션 md 파일을 다운받아 위와 같은 규칙을 지켜서 내가 손으로 배포했는데, origin 폴더 안에 넣으면 AI가 자동으로 저렇게 배포해주기를 원한다.

# 자동화 스크립트 사용법
1. 노션에서 마크다운으로 전체 페이지를 다운로드합니다. (하위 페이지 포함)
2. 다운로드한 압축 파일의 압축을 해제합니다.
3. 생성된 폴더를 이 프로젝트의 `origin` 폴더로 이동시킵니다.
4. 터미널에서 `python3 script.py` 명령어를 실행합니다.
5. 스크립트가 자동으로 `origin` 폴더 안의 모든 포스트를 처리하여 `_posts`와 `assets/images`로 옮기고, 원본은 `archive` 폴더로 이동시킵니다.

# 사용법
1. bundle install로 새로 생성
    * 권한이 없다면 sudo로
2. ouput에 있는 것을 업로드
3. bundle exec jekyll serve 로 로컬 실행

# 수정해서 업로드 방법
1. 내용 수정하고 `bundle exec jekyll build` 수행하면 `output`에 정적 파일 생성됨
2. `cd output`으로 `output` 디렉토리로 이동
3. `git add .` 로 변경사항 스테이징
4. `git commit -m "커밋 메시지"` 로 커밋
5. `git push origin HEAD:master` 로 원격 저장소에 푸시 (detached HEAD 상태일 경우)
6. `cd ..` 로 상위 디렉토리로 이동
7. `git add output` 로 서브모듈 변경사항 스테이징
8. `git commit -m "서브모듈 업데이트"` 로 커밋
9. `git push` 로 상위 저장소에 푸시

## 빌드 실패 및 포스트가 표시되지 않을 때 확인 사항
- **사이트맵(sitemap.xml) URL 문제:** `sitemap.xml` 파일에 `localhost` 주소가 포함되는 것을 방지하고, 실제 배포 URL(`https://leejigun.github.io`)이 올바르게 반영되도록 하려면 `bundle exec jekyll build` 명령 실행 시 `JEKYLL_ENV=production` 환경 변수를 함께 사용해야 합니다. 예: `JEKYLL_ENV=production bundle exec jekyll build`


- **날짜 문제:** 포스트의 `date`가 현재 시간보다 미래로 되어 있으면 빌드에서 제외됩니다. 로컬에서 확인하려면 `bundle exec jekyll build --future` 및 `bundle exec jekyll serve --future`와 같이 `--future` 옵션을 사용하세요.
- **머리말(Front Matter) 오류:** `title`과 같은 머리말 항목에 `**` 같은 마크다운 문법이 포함되면 빌드 오류가 발생할 수 있습니다. 머리말에는 순수한 텍스트만 사용하세요.

# tag 추가
1. _data/tags에 추가할 것
2. navigation바에 그 테그를 추가할 것
   1. _includes/navigation.html
   2. href="{{site.baseurl}}tag/ios/" 에서 ios 부분이 포스트의 tag 값이다.