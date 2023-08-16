from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# 파일이 실행될 때 환경변수에 현재 자신의 프로젝트의 settings.py파일 경로를 등록
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# 실행파일에 장고 환경을 불러옴
import django

django.setup()

# 크롤링을 하고 DB model에 저장
from naver.models import NaverData
from daum.models import DaumData


# 네이버
def fetch_naver_latest_data(page_count):
    result = []

    # 네이버뉴스 파이썬 검색결과
    base_url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%ED%8C%8C%EC%9D%B4%EC%8D%AC"

    # page_num = 페이지번호
    # page_count = 가져올 페이지 수
    # f 접두사를 붙이고 중괄호 {} 안에 변수나 표현식을 넣으면 해당 값을 문자열에 포함시킬 수 있음

    for page_num in range(1, page_count + 1):
        url = f"{base_url}&start={(page_num - 1) * 10}"
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # news_wrap 클래스를 가진 div 요소를 모두 찾아서 리스트 형태로 반환
        list_items = soup.find_all("div", "news_wrap")

        for item in list_items:
            # 기사제목
            title = item.find("a", "news_tit")["title"]

            # 링크
            page_link = item.find("a", "news_tit")["href"]
            page_link_parts = urlparse(page_link)

            # specific id 고유아이디 부여 -중복저장 안되게
            specific_id = page_link_parts.path.split("/")[-1]

            item_obj = {
                "title": title,
                "link": page_link,
                "specific_id": specific_id,
            }

            print(item_obj)
            result.append(item_obj)

    return result


def add_items_naver(crawled_items_naver):
    last_inserted_item = NaverData.objects.last()

    # 중복여부 확인
    if last_inserted_item:
        last_inserted_specific_id = last_inserted_item.specific_id
    else:
        last_inserted_specific_id = None

    items_to_insert_into_db = []

    for item in crawled_items_naver:
        if item["specific_id"] != last_inserted_specific_id:
            items_to_insert_into_db.append(item)

    # db에 저장
    for item in items_to_insert_into_db:
        NaverData(
            specific_id=item["specific_id"], title=item["title"], link=item["link"]
        ).save()

    return items_to_insert_into_db


# 다음
def fetch_daum_latest_data(page_count):
    result = []

    for page_num in range(1, page_count + 1):
        url = f"https://search.daum.net/search?nil_suggest=btn&w=news&DA=SBC&cluster=y&q=%ED%8C%8C%EC%9D%B4%EC%8D%AC&p={page_num}"
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        list_items = soup.find_all("div", class_="wrap_cont")

        for item in list_items:
            # title
            title = item.find("a", class_="tit_main fn_tit_u").text

            # link
            page_link = item.find("a", class_="tit_main fn_tit_u")["href"]
            page_link_parts = urlparse(page_link)

            # specific id 고유아이디 부여
            specific_id = page_link_parts.path.split("/")[-1]

            item_obj = {
                "title": title,
                "link": page_link,
                "specific_id": specific_id,
            }

            print(item_obj)
            result.append(item_obj)

    return result


def add_items_daum(crawled_items_daum):
    last_inserted_items = DaumData.objects.last()

    if last_inserted_items:
        last_inserted_specific_id = last_inserted_items.specific_id
    else:
        last_inserted_specific_id = None

    items_to_insert_into_db = []

    for item in crawled_items_daum:
        if item["specific_id"] != last_inserted_specific_id:
            items_to_insert_into_db.append(item)

    for item in items_to_insert_into_db:
        DaumData(
            specific_id=item["specific_id"], title=item["title"], link=item["link"]
        ).save()

    return items_to_insert_into_db


# 스크립트가 직접 실행될 때 아래의 코드 블록을 실행
if __name__ == "__main__":
    page_count = 10  # 크롤링할 페이지 수
    crawled_items_naver = fetch_naver_latest_data(page_count)
    crawled_items_daum = fetch_daum_latest_data(page_count)
    added_items_naver = add_items_naver(crawled_items_naver)
    added_items_daum = add_items_daum(crawled_items_daum)
    print(f"네이버에 추가된 아이템 수: {len(added_items_naver)}")
    print(f"다음에 추가된 아이템 수: {len(added_items_daum)}")
