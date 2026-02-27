import time
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_img_srcs(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(2)
    img_elements = driver.find_elements(By.CSS_SELECTOR, 'img.img_thumb')
    src_list = [img.get_attribute('src') for img in img_elements]
    driver.quit()
    return src_list

def main():
    url = "https://pf.kakao.com/_iyscG"
    srcs = get_img_srcs(url)
    filtered = [src for src in srcs if "k.kakaocdn.net" in src]
    img_url = None
    if len(filtered) >= 2:
        img_url = filtered[1]
    elif filtered:
        img_url = filtered[0]
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    img_filename = f"public/{today_str}.jpg"
    if img_url:
        response = requests.get(img_url)
        img_bytes = response.content
        with open(img_filename, "wb") as img_file:
            img_file.write(img_bytes)
        print(f"이미지가 {img_filename}로 저장되었습니다.")
        return True
    else:
        print("원본 이미지 URL을 찾을 수 없습니다.")
        return False

if __name__ == "__main__":
    for i in range(7):  # 9:00~9:30까지 5분 간격 7회
        try:
            if main():
                break
        except Exception as e:
            print(f"실패: {e}")
            if i < 6:
                time.sleep(300)  # 5분 대기
