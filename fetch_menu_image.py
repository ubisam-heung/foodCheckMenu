import os
import time
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# config_secret.py에서 민감 정보 import 
from config_secret import MENU_PAGE_URL, MENU2_PAGE_URL, IMG_DOMAIN_FILTER


def pick_first_restaurant(thumbs):
    """지하1층식당: 도메인 필터 후 두 번째 이미지(없으면 첫 번째)."""
    filtered = [t['src'] for t in thumbs if IMG_DOMAIN_FILTER in t['src']]
    if len(filtered) >= 2:
        return filtered[1]
    return filtered[0] if filtered else None


def pick_second_restaurant(thumbs):
    """2층식당(인스타그램): 가장 최근 게시물 이미지가 오늘의 메뉴."""
    srcs = [t['src'] for t in thumbs if t['src']]
    return srcs[0] if srcs else None


# 이름, 페이지 URL, 이미지 선택자, 이미지 선택 함수, 저장 폴더, 로딩 대기(초) (지하1층식당은 기존 경로 유지)
RESTAURANTS = [
    {'name': 'restaurant1', 'url': MENU_PAGE_URL, 'selector': 'img.img_thumb',
     'pick': pick_first_restaurant, 'dir': 'public', 'wait': 2},
    {'name': 'restaurant2', 'url': MENU2_PAGE_URL, 'selector': 'a[href*="/p/"] img',
     'pick': pick_second_restaurant, 'dir': 'public/r2', 'wait': 5},
]


def get_thumbs(driver, restaurant):
    driver.get(restaurant['url'])
    time.sleep(restaurant['wait'])
    return [
        {'src': img.get_attribute('src'), 'alt': img.get_attribute('alt') or ''}
        for img in driver.find_elements(By.CSS_SELECTOR, restaurant['selector'])
    ]


def fetch_one(driver, restaurant):
    thumbs = get_thumbs(driver, restaurant)
    img_url = restaurant['pick'](thumbs)
    if not img_url:
        print(f"[{restaurant['name']}] 원본 이미지 URL을 찾을 수 없습니다.")
        return False
    os.makedirs(restaurant['dir'], exist_ok=True)
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    img_filename = f"{restaurant['dir']}/{today_str}.jpg"
    response = requests.get(img_url)
    response.raise_for_status()
    with open(img_filename, "wb") as img_file:
        img_file.write(response.content)
    print(f"[{restaurant['name']}] 이미지가 {img_filename}로 저장되었습니다.")
    return True


def main(pending):
    """pending 식당들을 처리하고, 실패한 식당 목록을 반환."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    failed = []
    try:
        for restaurant in pending:
            try:
                if not fetch_one(driver, restaurant):
                    failed.append(restaurant)
            except Exception as e:
                print(f"[{restaurant['name']}] 실패: {e}")
                failed.append(restaurant)
    finally:
        driver.quit()
    return failed


if __name__ == "__main__":
    pending = RESTAURANTS
    for i in range(7):  # 5분 간격 7회
        pending = main(pending)
        if not pending:
            break
        if i < 6:
            time.sleep(300)  # 5분 대기
