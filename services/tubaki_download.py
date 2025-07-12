
# ✅ 標準ライブラリ
import time
import calendar
from datetime import datetime, timedelta

# ✅ 外部ライブラリ（Selenium）
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ 自作モジュール
import sys
sys.path.append(r"C:\Users\daiki\source\repos\st-project\st-project")

import db.db_logic as db_logic
from untils.until import logic

def move_wait(ec):
    try:
        # 指定した要素が表示されるまで最大10秒待機
        element = WebDriverWait(driver, 15).until(ec)
        print("画面が遷移しました。:", element.text)
    except Exception as e:
        print("画面が遷移しませんでした:", e)

def get_jigetu(year, month):
    if month == 12:
        month = 1
    else:
        month += 1
    return calendar.monthrange(year, month)[1]

def insert_reservation_status(day, last_day_of_month, target_day):
    # 全てのクリック可能な日付を繰り返し
    formatted_today = target_day.strftime("%Y-%m-%d")

    for i in range(day, last_day_of_month + 1):
        query_list = []
        query_list.clear()
        clickable_days = driver.find_element(By.LINK_TEXT, str(i))
        clickable_days.click()
        time.sleep(2)
        # 予約状況を取得
        image_elements = driver.find_elements(By.CSS_SELECTOR, "tr td.time-table2 img ")
        yoyaku_list = [img.get_attribute("alt") for img in image_elements]
        court_no = 1
        cnt = 0
        for yoyaku in yoyaku_list:
            cnt = logic.get_insert_query(cnt, f'テニスコート{court_no}', formatted_today, yoyaku, query_list)
            if cnt == 0:
                court_no += 1
        target_day = target_day + timedelta(days=1)
        formatted_today = target_day.strftime("%Y-%m-%d")

        db_logic.exec_query_list(query_list)
    

# 今日の日付を取得
now_dt = datetime.now()
year = now_dt.year
month = now_dt.month
day = now_dt.day
today = datetime.today()

# その月の日数(月末日)を取得
last_day_of_month = calendar.monthrange(year, month)[1]

# WebDriverのセットアップ
# options = webdriver.ChromeOptions()
options = Options()
options.add_argument("--headless")  # 画面非表示

try:

    driver = webdriver.Chrome(options=options)# WebDriverのセットアップ (ChromeDriverを例に)

    # ターゲットのWebページを開く
    driver.get("https://www.yoyaku.city.matsuyama.ehime.jp/user/")

    # 検索画面へ遷移
    move_search_button = driver.find_element(By.XPATH, '//img[@alt="施設名から"]')
    move_search_button.click()

    # 画面移動を待機
    move_wait(EC.presence_of_element_located((By.ID, 'textKeyword')))

    # 検索条件入力
    shisetu_text_area = driver.find_element(By.ID, 'textKeyword')
    shisetu_text_area.send_keys("河野別府公園")

    # 検索ボタン押下
    search_button = driver.find_element(By.XPATH, '//input[@value="上記の内容で検索する"]')
    search_button.click()
    # 選択ボタンを取得 (例えば、ボタンのユニークな属性を使用する)
    select_button = driver.find_element(By.XPATH, "//input[@type='button' and @value='選択']")
    # 選択ボタンをクリック
    select_button.click()

    # 画面移動を待機
    move_wait(EC.presence_of_element_located((By.XPATH, "//font[@class='font-navy' and contains(text(), '●テニスコート１')]")))

    # テニスコード以外のチェックを外す
    check_box1 = driver.find_element(By.XPATH, '//input[@value="10805010"]')
    check_box2 = driver.find_element(By.XPATH, '//input[@value="10805020"]')
    # チェックされている場合は外す
    if check_box1.is_selected():
        check_box1.click()
        move_wait(EC.element_to_be_clickable((By.XPATH, '//input[@value="10805020"]')))
    if check_box2.is_selected():
        check_box2.click()
    print("テニスコート以外のチェックを外しました。")

    # 表示の反映ボタンクリック
    reload_button = driver.find_element(By.ID, 'doReload')
    reload_button.click()
    move_wait(EC.element_to_be_clickable((By.ID, 'doReload')))

    print("表示の反映ボタンをクリックしました。")

    # 全検削除してから挿入
    db_logic.delete_table()
    
    insert_reservation_status(day, last_day_of_month, today)
    print("当月分をデータベースに反映しました。")

    # "次月"というリンクテキストを持つ要素を探してクリック
    next_month_button = driver.find_element(By.LINK_TEXT, "次月")
    next_month_button.click()
    print("「次月」ボタンをクリックしました。")
    time.sleep(5)
    
    # 次月の日数(月末日)を取得
    last_day_of_month = get_jigetu(year, month)
    print("次月を取得しました。")
    # 翌月1日を計算
    next_month = today.replace(day=1) + timedelta(days=32)  # 次の月を超える日数を足す
    first_of_next_month  = next_month.replace(day=1)
    insert_reservation_status(1, last_day_of_month, first_of_next_month)
    print("次月分をデータベースに反映しました。")
    print("処理完了。")

except Exception as e:
    print(f"クリックに失敗: {e}")
    driver.quit()

# 終了処理
driver.quit()

