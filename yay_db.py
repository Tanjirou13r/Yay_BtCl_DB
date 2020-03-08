# -*- coding: utf-8 -*-
import os, time, pickle, sys, logging, re, random, threading, configparser, requests, json, schedule
#画像ダウンロード
from urllib import request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

#----------------------------------------------------------------------------------------------------#
###ログインするアカウント情報、設定###
alive = True

# --------------------------------------------------
# configparserの宣言とiniファイルの読み込み
# --------------------------------------------------
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

mode = config_ini.getint('Mode', 'mode')
email1 = config_ini.get('MainAccount', 'email1')
password1 = config_ini.get('MainAccount', 'password1')
t_email1 = config_ini.get('MainAccount', 't_email1')
t_password1 = config_ini.get('MainAccount', 't_password1')
os.makedirs("cache/"+email1, exist_ok=True)

email2 = config_ini.get('SubAccount', 'email2')
password2 = config_ini.get('SubAccount', 'password2')
t_email2 = config_ini.get('SubAccount', 't_email2')
t_password2 = config_ini.get('SubAccount', 't_password2')
if mode == 2:
    os.makedirs("cache/"+email2, exist_ok=True)


#loggingモジュール設定
#コンソールにログを出力するハンドラー
stream_log = logging.StreamHandler()
stream_log.setLevel(logging.INFO)
stream_log.setFormatter(logging.Formatter('[%(levelname)s](%(lineno)s)：%(message)s'))
#ファイルにログを出力するハンドラー
file_log = logging.FileHandler(filename='logger.log')
file_log.setLevel(logging.INFO)
file_log.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s](%(filename)s:%(lineno)s)：%(message)s'))
#getLogger()でrootロガーを取得し、ハンドラーを設定
logging.getLogger().addHandler(stream_log)
logging.getLogger().addHandler(file_log)
#rootロガーのログレベルは、ハンドラーの中で一番低いものを指定しておく
#こうしておかないと、子ハンドラーにエラーが伝播しない
logging.getLogger().setLevel(logging.DEBUG)

#----------------------------------------------------------------------------------------------------#

#ブラウザ起動
options = Options()
options.add_argument('--headless') #ヘッドレスモードを有効
options.add_argument('--no-sandbox') #Sandboxの外でプロセスを動作(セキュリティ無効化)
options.add_argument('--disable-gpu') #GPU機能を無効化
options.add_argument('--window-size=1280,1024') #ウィンドウサイズの調整
driver1_1 = webdriver.Chrome(options=options)
driver1_2 = webdriver.Chrome(options=options)
driver1_3 = webdriver.Chrome(options=options)
driver1_4 = webdriver.Chrome(options=options)
if mode == 2:
    driver2_1 = webdriver.Chrome(options=options)
    driver2_2 = webdriver.Chrome(options=options)
    driver2_3 = webdriver.Chrome(options=options)

#Yay!サーバー接続確認
try:
    logging.info("Browser1_1 and Browser1_2 Connection check...")
    driver1_1.get('https://yay.space/timeline/following')
    WebDriverWait(driver1_1, 5).until(EC.presence_of_all_elements_located)
    driver1_2.get('https://yay.space/timeline/following')
    WebDriverWait(driver1_2, 5).until(EC.presence_of_all_elements_located)
    driver1_3.get('https://yay.space/timeline/following')
    WebDriverWait(driver1_3, 5).until(EC.presence_of_all_elements_located)
    driver1_4.get('https://yay.space/timeline/following')
    WebDriverWait(driver1_4, 5).until(EC.presence_of_all_elements_located)
    if mode == 2:
        logging.info("Browser2_1 Connection check...")
        driver2_1.get('https://yay.space/timeline/following')
        WebDriverWait(driver2_1, 5).until(EC.presence_of_all_elements_located)
        driver2_2.get('https://yay.space/timeline/following')
        WebDriverWait(driver2_2, 5).until(EC.presence_of_all_elements_located)
        driver2_3.get('https://yay.space/timeline/following')
        WebDriverWait(driver2_3, 5).until(EC.presence_of_all_elements_located)
    logging.info("All Connected successfully...")
except:
    logging.error("Browser Connection timed out...!!")
    sys.exit()

#----------------------------------------------------------------------------------------------------#

###アカウントログイン###
def login():

    #メインアカウント
    try:
        #ログイン状況チェック
        logging.info("Check MainAccount login status...")
        cookies = pickle.load(open("cache/" + email1 + "/cookies.pkl", "rb"))
        for cookie in cookies:
            driver1_1.add_cookie(cookie)
            driver1_2.add_cookie(cookie)
            driver1_3.add_cookie(cookie)
            driver1_4.add_cookie(cookie)
        driver1_1.refresh()
        driver1_2.refresh()
        driver1_3.refresh()
        driver1_4.refresh()
        WebDriverWait(driver1_1, 5).until(EC.presence_of_all_elements_located)
        WebDriverWait(driver1_2, 5).until(EC.presence_of_all_elements_located)
        WebDriverWait(driver1_3, 5).until(EC.presence_of_all_elements_located)
        WebDriverWait(driver1_4, 5).until(EC.presence_of_all_elements_located)
        driver1_1.find_element_by_class_name('Header__profile__a')
        driver1_2.find_element_by_class_name('Header__profile__a')
        driver1_3.find_element_by_class_name('Header__profile__a')
        driver1_4.find_element_by_class_name('Header__profile__a')
        logging.info("Logged in to MainAccount from saved information...")
    except:
        #ログインされていない場合
        try:
            logging.info("Browser1_1 Move page...")
            driver1_1.get('https://yay.space/login')
            WebDriverWait(driver1_1, 5).until(EC.presence_of_all_elements_located)
        except:
            logging.error("Browser1_1 Connection timed out...!!")
            sys.exit()

        #ログイン情報記入 > ログインボタンクリック
        logging.info("Browser1_1 Start login...")
        driver1_1.find_element_by_name('email').send_keys(email1)
        driver1_1.find_element_by_name('password').send_keys(password1)
        driver1_1.find_element_by_class_name('Button.Button--less-rounded.Button--icon-login').click()
        #ログイン読み込み待ち
        for _ in range(50):
            if driver1_1.current_url == "https://yay.space/timeline/following":
                break
            else:
                time.sleep(0.1)
        else:
            logging.error("Browser1_1 Connection timed out...!!")
            sys.exit()

        #ログインクッキー保存
        pickle.dump(driver1_1.get_cookies() , open("cache/" + email1 + "/cookies.pkl","wb"))
        logging.info("Browser1_1 Login completed...")

        #ブラウザー2,3 クッキーからログイン
        logging.info("Browser1_2 and Browser1_3 Start login...")
        cookies = pickle.load(open("cache/" + email1 + "/cookies.pkl", "rb"))
        for cookie in cookies:
            driver1_2.add_cookie(cookie)
            driver1_3.add_cookie(cookie)
            driver1_4.add_cookie(cookie)
        driver1_2.refresh()
        driver1_3.refresh()
        driver1_4.refresh()
        WebDriverWait(driver1_2, 5).until(EC.presence_of_all_elements_located)
        WebDriverWait(driver1_3, 5).until(EC.presence_of_all_elements_located)
        WebDriverWait(driver1_4, 5).until(EC.presence_of_all_elements_located)
        driver1_2.find_element_by_class_name('Header__profile__a')
        driver1_3.find_element_by_class_name('Header__profile__a')
        driver1_4.find_element_by_class_name('Header__profile__a')
        logging.info("Browser1_2 and Browser1_3 Login completed...")

    #サブアカウント
    if mode == 2:
        try:
            #ログイン状況チェック
            logging.info("Check SubAccount login status...")
            cookies = pickle.load(open("cache/" + email2 + "/cookies.pkl", "rb"))
            for cookie in cookies:
                driver2_1.add_cookie(cookie)
                driver2_2.add_cookie(cookie)
                driver2_3.add_cookie(cookie)
            driver2_1.refresh()
            driver2_2.refresh()
            driver2_3.refresh()
            WebDriverWait(driver2_1, 5).until(EC.presence_of_all_elements_located)
            WebDriverWait(driver2_2, 5).until(EC.presence_of_all_elements_located)
            WebDriverWait(driver2_3, 5).until(EC.presence_of_all_elements_located)
            driver2_1.find_element_by_class_name('Header__profile__a')
            driver2_2.find_element_by_class_name('Header__profile__a')
            driver2_3.find_element_by_class_name('Header__profile__a')
            logging.info("Logged in to SubAccount from saved information...")
        except:
            #ログインされていない場合
            try:
                logging.info("Browser2_1 Move page...(Yay!ログインページ)")
                driver2_1.get('https://yay.space/login')
                WebDriverWait(driver2_1, 5).until(EC.presence_of_all_elements_located)
            except:
                logging.error("Browser2_1 Connection timed out...!!")
                sys.exit()

            #ログイン情報記入 > ログインボタンクリック
            logging.info("Browser2_1 Start login...")
            driver2_1.find_element_by_name('email').send_keys(email2)
            driver2_1.find_element_by_name('password').send_keys(password2)
            driver2_1.find_element_by_class_name('Button.Button--less-rounded.Button--icon-login').click()
            #ログイン読み込み待ち
            for _ in range(50):
                if driver2_1.current_url == "https://yay.space/timeline/following":
                    break
                else:
                    time.sleep(0.1)
            else:
                logging.error("Browser2_1 Connection timed out...!!")
                sys.exit()

            #ログインクッキー保存
            pickle.dump(driver2_1.get_cookies() , open("cache/" + email2 + "/cookies.pkl","wb"))
            logging.info("Browser2_1 Login completed...")

            #ブラウザー3 クッキーからログイン
            logging.info("Browser2_2 and Browser2_3 Start login...")
            cookies = pickle.load(open("cache/" + email2 + "/cookies.pkl", "rb"))
            for cookie in cookies:
                driver2_2.add_cookie(cookie)
                driver2_3.add_cookie(cookie)
            driver2_2.refresh()
            driver2_3.refresh()
            WebDriverWait(driver2_2, 5).until(EC.presence_of_all_elements_located)
            WebDriverWait(driver2_3, 5).until(EC.presence_of_all_elements_located)
            driver2_2.find_element_by_class_name('Header__profile__a')
            driver2_3.find_element_by_class_name('Header__profile__a')
            logging.info("Browser2_2 and Browser2_3 Login completed...")

#----------------------------------------------------------------------------------------------------#

    #ログインユーザーのステータス
    my_id = driver1_1.find_element_by_class_name('Header__profile__a').get_attribute("href")
    my_name = driver1_1.find_element_by_class_name('Nickname__span').text
    try:
        driver1_1.find_element_by_class_name('ImageLoader.Avatar.Avatar--vip')
        d_vip = "Enable"
    except:
        d_vip = "Disable"
    if mode == 1:
        logging.info("Login Status\n< Main Account >\nUSERID:["+my_id.replace("https://yay.space", "") + "] NAME:["+my_name + "] VIP:"+d_vip + "\n")

    if mode == 2:
        sub_my_id = driver2_1.find_element_by_class_name('Header__profile__a').get_attribute("href")
        sub_my_name = driver2_1.find_element_by_class_name('Nickname__span').text
        try:
            driver2_1.find_element_by_class_name('ImageLoader.Avatar.Avatar--vip')
            sub_d_vip = "Enable"
        except:
            sub_d_vip = "Disable"
        logging.info("Login Status\n< Main Account >\nUSERID:["+my_id.replace("https://yay.space", "") + "] NAME:["+my_name + "] VIP:"+d_vip +
        "\n< Sub Account >\nUSERID:["+sub_my_id.replace("https://yay.space", "") + "] NAME:["+sub_my_name + "] VIP:"+sub_d_vip + "\n")

#----------------------------------------------------------------------------------------------------#

# 前日比の自動投稿
def job():
    print("\nスタート\n")
    # driver1_4 のページリロード
    driver1_4.find_element_by_class_name('Header__profile').click()
    WebDriverWait(driver1_4, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[1]/div/div/div')))
    # 現在の値を取得
    n_posts = driver1_4.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/div[1]/div/div[2]/dl/div[1]/a/dd').text
    n_follow = driver1_4.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/div[1]/div/div[2]/dl/div[4]/a/dd').text
    n_follower = driver1_4.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/div[1]/div/div[2]/dl/div[3]/a/dd').text
    n_letter = driver1_4.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/div[1]/div/div[2]/dl/div[2]/a/dd').text

    # jsonを読み込み、計算
    with open("cache/" + email1 + "/comparison_date.json") as f:
        date = json.load(f)
    posts = int(n_posts.replace(",", "")) - date["posts"]
    follow = int(n_follow.replace(",", "")) - date["follow"]
    follower = int(n_follower.replace(",", "")) - date["follower"]
    letter = int(n_letter.replace(",", "")) - date["letter"]
    y_posts = date["yesterday_posts"] - posts
    y_follow = date["yesterday_follow"] - follow
    y_follower = date["yesterday_follower"] - follower
    y_letter = date["yesterday_letter"] - letter

    # 前日比を投稿
    sent = """こちらは前日比の集計結果です。
投稿した数 : {0}（前日比 : {1}）
フォローした数 : {2}（前日比 : {3}）
フォローされた数 : {4}（前日比 : {5}）
レターされた数 : {6}（前日比 : {7}）
""".format(posts, y_posts, follow, y_follow, follower, y_follower, letter, y_letter)

    driver1_4.get("https://yay.space/timeline/following")
    WebDriverWait(driver1_4, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div[1]/form/div/div[1]/textarea')))
    driver1_4.find_element_by_class_name('PostBox__body.PostBox__body--color-0.PostBox__body--fz-0').click()
    for sent_text in sent.splitlines():
        driver1_4.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/div[1]/form/div/div[1]/div').send_keys(sent_text)
        driver1_4.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/div[1]/form/div/div[1]/div').send_keys(Keys.SHIFT, Keys.ENTER)
    driver1_4.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/div[1]/form/div/div[1]/div').send_keys(Keys.ENTER)

    # 現在の値を書き込み、保存
    str = {"posts": int(n_posts.replace(",", "")), "likes": 0, "follow": int(n_follow.replace(",", "")), "follower": int(n_follower.replace(",", "")), "rt_to": 0, "rt_me": 0, "letter": int(n_letter.replace(",", "")), "yesterday_posts": posts, "yesterday_likes": 0, "yesterday_follow": follow, "yesterday_follower": follower, "yesterday_rt_to": 0, "yesterday_rt_me": 0, "yesterday_letter": letter}
    with open("cache/" + email1 + "/comparison_date.json", mode='w') as f:
        json.dump(str, f, indent=2, ensure_ascii=False)
def auto_conpari():
    schedule.every().day.at(config_ini.get('Mode', 'TimeToPost')).do(job)
    while alive:
        schedule.run_pending()
        time.sleep(5)

#----------------------------------------------------------------------------------------------------#

def main():

    #コマンドリスト
    commands = ["help","speed","userid","icon","cover"]


    #チャットページ 接続
    try:
        driver1_2.get('https://yay.space/timeline/all?modalMode=1')
        WebDriverWait(driver1_2, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modals"]/div[1]/div/div[2]/dl/a[1]')))
    except:
        logging.error("Connection timed out...!!")
        sys.exit()


    #チャット監視
    while alive:
        try:
            #チャット画面の1番上部、textを監視
            text_s = driver1_2.find_element_by_class_name('RecommendUsers__item.RecommendUsers__item--chatroom')
            #textオブジェクト以外のエラー回避
            text = text_s.find_element_by_class_name('RecommendUsers__item__p').text
        except:
            continue


        if text in commands:
            text_s.find_element_by_class_name('RecommendUsers__item__p').click()
            WebDriverWait(driver1_2, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modals"]/div[1]/div/div[2]/div/div/p[1]')))
            last_mes = driver1_2.find_elements_by_class_name('Messages__item.Messages__item--self')[-1]
            try: last_text = (last_mes.find_element_by_class_name('Messages__item__span.Messages__item__span--text').text).split("\n")[0]
            except: continue

            if last_text == "help":
                driver1_2.find_element_by_class_name('ReplyForm__input').send_keys("以下のコマンドが使用できます")
                driver1_2.find_element_by_class_name('ReplyForm__input').send_keys(Keys.SHIFT, Keys.ENTER)
                driver1_2.find_element_by_class_name('ReplyForm__input').send_keys("help：コマンド表を表示します")
                driver1_2.find_element_by_class_name('ReplyForm__input').send_keys(Keys.SHIFT, Keys.ENTER)
                driver1_2.find_element_by_class_name('ReplyForm__input').send_keys("speed：処理速度を計測します")
                driver1_2.find_element_by_class_name('ReplyForm__input').send_keys(Keys.SHIFT, Keys.ENTER)
                driver1_2.find_element_by_class_name('ReplyForm__input').send_keys("userid：チャット相手のUserIDを確認します")
                driver1_2.find_element_by_class_name('ReplyForm__input').send_keys(Keys.SHIFT, Keys.ENTER)
                driver1_2.find_element_by_class_name('ReplyForm__input').send_keys("icon：チャット相手のアイコンを送信します")
                driver1_2.find_element_by_class_name('ReplyForm__input').send_keys(Keys.SHIFT, Keys.ENTER)
                driver1_2.find_element_by_class_name('ReplyForm__input').send_keys("cover：チャット相手の背景を送信します")
                driver1_2.find_element_by_class_name('Button.Button--green.Button--icon-chat-send.Button--wrap-content').click()

            elif last_text == "speed":
                start = time.time()
                driver1_2.find_element_by_class_name('ReplyForm__input').send_keys("Measuring...")
                driver1_2.find_element_by_class_name('Button.Button--green.Button--icon-chat-send.Button--wrap-content').click()
                elapsed_time = time.time() - start
                driver1_2.find_element_by_class_name('ReplyForm__input').send_keys("{0}[sec]".format(elapsed_time))
                driver1_2.find_element_by_class_name('Button.Button--green.Button--icon-chat-send.Button--wrap-content').click()

            elif last_text == "userid":
                op_userid = driver1_2.find_element_by_class_name('Modal__header__h2__a').get_attribute("href")
                driver1_2.find_element_by_class_name('ReplyForm__input').send_keys(op_userid.replace("https://yay.space", ""))
                driver1_2.find_element_by_class_name('Button.Button--green.Button--icon-chat-send.Button--wrap-content').click()

            elif last_text == "icon":
                y_header = driver1_2.find_element_by_class_name('Modal__header__h2__a')
                URL = y_header.find_element_by_class_name('ImageLoader.Avatar').get_attribute("data-url")
                request.urlretrieve(URL, "icon.jpg")
                driver1_2.find_element(By.XPATH, '//input[@type="file"]').send_keys("/root/yay/icon.jpg")
                while True:
                    last_mes = driver1_2.find_elements_by_class_name('Messages__item.Messages__item--self')[-1]
                    try:
                        last_mes.find_element_by_class_name('Messages__item__span.Messages__item__span--eternal_image')
                        break
                    except: pass
            """
            elif last_text == "cover":
                driver1_2.find_element_by_class_name('Modal__header__h2').click()
                WebDriverWait(driver1_2, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div[1]/div/div[1]/figure')))
                URL = driver1_2.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/div[1]/div/div[1]/figure').get_attribute("style")
                driver1_2.save_screenshot('screenshot.png')
                logging.info(URL)
                request.urlretrieve(URL[23:-3], "cover.jpg")
                driver1_2.back()
                WebDriverWait(driver1_2, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modals"]/div[1]/div/div[2]/div/div/p[1]')))
                driver1_2.find_element(By.XPATH, '//input[@type="file"]').send_keys("/root/yay/cover.jpg")
                while True:
                    last_mes = driver1_2.find_elements_by_class_name('Messages__item.Messages__item--self')[-1]
                    try:
                        last_mes.find_element_by_class_name('Messages__item__span.Messages__item__span--eternal_image')
                        break
                    except: pass
            """

            driver1_2.get('https://yay.space/timeline/all?modalMode=1')
            WebDriverWait(driver1_2, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modals"]/div[1]/div/div[2]/dl/a[1]')))

#----------------------------------------------------------------------------------------------------#

def main_sub():

    #チャットページ 接続
    try:
        driver2_2.get('https://yay.space/timeline/all?modalMode=1')
        WebDriverWait(driver2_2, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modals"]/div[1]/div/div[2]/dl/a[1]')))
    except:
        logging.error("Connection timed out...!!")
        sys.exit()


    #チャット監視
    while alive:
        x = 0
        while x <= 40 and alive:
            try:
                #チャット画面の1番上部、textを監視
                try: text_s = driver2_2.find_elements_by_class_name('RecommendUsers__item.RecommendUsers__item--chatroom')[x]
                except:
                    x = 0
                    continue
                x = x + 1
                try: text_s.find_element_by_class_name('Badge')
                except: continue
                #textオブジェクト以外のエラー回避
                text = text_s.find_element_by_class_name('RecommendUsers__item__p').text
            except:
                #textオブジェクト以外は既読して戻る
                text_s.find_element_by_class_name('RecommendUsers__item__p').click()
                WebDriverWait(driver2_2, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modals"]/div[1]/div/div[2]/div/div/p[1]')))
                driver2_2.get('https://yay.space/timeline/all?modalMode=1')
                WebDriverWait(driver2_2, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modals"]/div[1]/div/div[2]/dl/a[1]')))
                continue


            text_s.find_element_by_class_name('RecommendUsers__item__p').click()
            WebDriverWait(driver2_2, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modals"]/div[1]/div/div[2]/div/div/p[1]')))
            last_mes = driver2_2.find_elements_by_class_name('Messages__item')[-1]
            try: last_text = (last_mes.find_element_by_class_name('Messages__item__span.Messages__item__span--text').text).split("\n")[0]
            except:
                driver2_2.get('https://yay.space/timeline/all?modalMode=1')
                WebDriverWait(driver2_2, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modals"]/div[1]/div/div[2]/dl/a[1]')))
                continue

            payload = {'apikey':'DZZF3AKLPDL2kxbRRWXwvIwxbGUWEZQ7', 'query':last_text}
            r = requests.request("POST", "https://api.a3rt.recruit-tech.co.jp/talk/v1/smalltalk", data=payload).json()
            try: driver2_2.find_element_by_class_name('ReplyForm__input').send_keys(str(r['results'][0]['reply']))
            except: pass
            driver2_2.find_element_by_class_name('Button.Button--green.Button--icon-chat-send.Button--wrap-content').click()

            driver2_2.get('https://yay.space/timeline/all?modalMode=1')
            try: WebDriverWait(driver2_2, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modals"]/div[1]/div/div[2]/dl/a[1]')))
            except: continue


#----------------------------------------------------------------------------------------------------#

def auto_c():

    #みんなの投稿ページ 接続
    if mode == 1:
        try:
            driver1_1.get('https://yay.space/timeline/all')
            WebDriverWait(driver1_1, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div[2]/dl/div[1]')))
        except:
            logging.error("Browser1_1 Connection timed out...!!")
            sys.exit()
    if mode == 2:
        try:
            driver1_1.get('https://yay.space/timeline/all')
            driver2_1.get('https://yay.space/timeline/all')
            WebDriverWait(driver1_1, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div[2]/dl/div[1]')))
            WebDriverWait(driver2_1, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div[2]/dl/div[1]')))
        except:
            logging.error("Browser1_1 or Browser2_1 Connection timed out...!!")
            sys.exit()


    ###みんなの投稿 自動いいね繰り返し実行###

    sel = 1 #2アカウント時の交換用
    c_ok1 = 0 #いいね合計カウント（メイン）
    c_ok2 = 0#いいね合計カウント（サブ）
    c_all1 = 0 #選択されたみんなの投稿合計カウント（メイン）
    c_all2 = 0 #選択されたみんなの投稿合計カウント（サブ）

    while alive:

        ok_list = [] #いいね済みのリスト
        z = 1 #1ページに存在する投稿のいいね制限用

        while z <= 15 and alive:

            z = z + 1
            if sel == 1:
                #ひとつのタイムラインに対して要素を選択
                element = driver1_1.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/div[2]/dl/div[{}]'.format(z))
                #選択された要素までスクロール
                actions = ActionChains(driver1_1)
                actions.move_to_element(element)
                actions.perform()
                postid = element.find_element_by_class_name('Timeline__item__handle').get_attribute("href")
                userid = element.find_element_by_class_name('Timeline__item__profile-img__a').get_attribute("href")
                #いいね済みのスルー
                if postid.replace("https://yay.space/post/", "") in ok_list:
                    continue
                try:
                    element.find_element_by_class_name('Heart__path.Heart__path--liked')
                    continue
                except: pass
                #選択されたいいね済み以外みんなの投稿合計カウント
                c_all1 = c_all1 + 1
                #リプライ投稿のスルー
                try:
                    element.find_element_by_class_name('ReplyTo')
                    continue
                except: pass
                #だれ通募集投稿のスルー
                try:
                    element.find_element_by_class_name('Timeline__item__call')
                    continue
                except: pass

            if sel == 2:
                #ひとつのタイムラインに対して要素を選択
                element1 = driver2_1.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/div[2]/dl/div[{}]'.format(z))
                #選択された要素までスクロール
                actions = ActionChains(driver2_1)
                actions.move_to_element(element1)
                actions.perform()
                postid1 = element1.find_element_by_class_name('Timeline__item__handle').get_attribute("href")
                userid1 = element1.find_element_by_class_name('Timeline__item__profile-img__a').get_attribute("href")
                #いいね済みのスルー
                if postid1.replace("https://yay.space/post/", "") in ok_list:
                    continue
                try:
                    element1.find_element_by_class_name('Heart__path.Heart__path--liked')
                    continue
                except: pass
                #選択されたいいね済み以外みんなの投稿合計カウント
                c_all2 = c_all2 + 1
                #リプライ投稿のスルー
                try:
                    element1.find_element_by_class_name('ReplyTo')
                    continue
                except: pass
                #だれ通募集投稿のスルー
                try:
                    element1.find_element_by_class_name('Timeline__item__call')
                    continue
                except: pass


            #いいね実行
            if sel == 1:
                try:
                    element.find_element_by_class_name('Heart__path').click()
                    c_ok1 = c_ok1 + 1
                    ok_list.append(postid.replace("https://yay.space/post/", ""))
                except: continue
            if mode == 2 and sel == 2:
                try:
                    element1.find_element_by_class_name('Heart__path').click()
                    c_ok2 = c_ok2 + 1
                    ok_list.append(postid1.replace("https://yay.space/post/", ""))
                except: continue
            if sel == 1 and mode == 2: sel = 2
            else:
                if sel == 2: sel = 1


            if mode == 1:
                print("< Auto Like >\n（Main Account）\nUserID:{0} PostID:{1}".format(userid.replace("https://yay.space", ""), postid.replace("https://yay.space", "")) + "\n合計カウント（いいね/全投稿）：{0} / {1}\r\033[4A".format(c_ok1, c_all1))
            if mode == 2:
                if c_all2 > 1:
                    print("< Auto Like >\n（Main Account）\nUserID:{0} PostID:{1}".format(userid.replace("https://yay.space", ""), postid.replace("https://yay.space", "")) + "\n合計カウント（いいね/全投稿）：{0} / {1}".format(c_ok1, c_all1)
                    + "\n（Sub Account）\nUserID:{0} PostID:{1}".format(userid1.replace("https://yay.space", ""), postid1.replace("https://yay.space", "")) + "\n合計カウント（いいね/全投稿）：{0} / {1}\r\033[7A".format(c_ok2, c_all2))
                else:
                    print("< Auto Like >\n（Main Account）\nUserID:{0} PostID:{1}".format(userid.replace("https://yay.space", ""), postid.replace("https://yay.space", "")) + "\n合計カウント（いいね/全投稿）：{0} / {1}\r\033[4A".format(c_ok1, c_all1))


            #いいねする間隔調整
            if mode == 1:
                time.sleep(2)
            if mode == 2:
                time.sleep(1)


        #みんなの投稿ページリロード
        for _ in range(3):  # 最大3回実行
            try:
                if mode == 1:
                    driver1_1.refresh()
                    WebDriverWait(driver1_1, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div[2]/dl/div[1]')))
                if mode == 2:
                    driver1_1.refresh()
                    driver2_1.refresh()
                    WebDriverWait(driver1_1, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div[2]/dl/div[1]')))
                    WebDriverWait(driver2_1, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div[2]/dl/div[1]')))
            except Exception as e:
                pass  # 必要であれば失敗時の処理
            else:
                print("\nPage reload..." + "\r\033[2A")
                z = 1
                break  # 失敗しなかった時はループを抜ける
        else:
            logging.error("Reload failed...!!")
            return

#----------------------------------------------------------------------------------------------------#

def auto_share():

    """
    #ユーザー検索ページ接続 > シェアボタンクリック
    if mode == 1:
        try:
            driver1_3.get('https://yay.space/users/search')
            WebDriverWait(driver1_3, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div[2]/div[1]/a')))
            parent_window1_3 = driver1_3.current_window_handle
        except:
            logging.error("Browser1_3 Connection timed out...!!")
            sys.exit()
        driver1_3.find_element_by_class_name('Box__header__a').click()
        WebDriverWait(driver1_3, 5).until(lambda d: len(d.window_handles) > 1)
        driver1_3.switch_to.window(driver1_3.window_handles[1])

    if mode == 2:
        try:
            driver1_3.get('https://yay.space/users/search')
            driver2_3.get('https://yay.space/users/search')
            WebDriverWait(driver1_3, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div[2]/div[1]/a')))
            WebDriverWait(driver2_3, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div[2]/div[1]/a')))
            parent_window1_3 = driver1_3.current_window_handle
            parent_window2_3 = driver2_3.current_window_handle
        except:
            logging.error("Browser1_3 or Browser2_3 Connection timed out...!!")
            sys.exit()
        driver1_3.find_element_by_class_name('Box__header__a').click()
        driver2_3.find_element_by_class_name('Box__header__a').click()
        WebDriverWait(driver1_3, 5).until(lambda d: len(d.window_handles) > 1)
        WebDriverWait(driver2_3, 5).until(lambda d: len(d.window_handles) > 1)
        driver1_3.switch_to.window(driver1_3.window_handles[1])
        driver2_3.switch_to.window(driver2_3.window_handles[1])


    #Twitterログイン
    try:
        cookies = pickle.load(open("cache/" + email1 + "/cookies_t.pkl", "rb"))
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
                driver1_3.add_cookie(cookie)
        driver1_3.refresh()
        WebDriverWait(driver1_3, 5).until(EC.presence_of_element_located((By.ID, 'session')))
    except:
        driver1_3.find_element_by_name('session[username_or_email]').send_keys(t_email1)
        driver1_3.find_element_by_name('session[password]').send_keys(t_password1)
        driver1_3.find_element_by_name('remember_me').click()
        driver1_3.find_element_by_class_name('button.selected.submit').click()
        WebDriverWait(driver1_3, 5).until(EC.presence_of_element_located((By.ID, 'session')))
        pickle.dump(driver1_3.get_cookies() , open("cache/" + email1 + "/cookies_t.pkl","wb"))

    if mode == 2:
        try:
            cookies = pickle.load(open("cache/" + email2 + "/cookies_t.pkl", "rb"))
            for cookie in cookies:
                if 'expiry' in cookie:
                    del cookie['expiry']
                    driver2_3.add_cookie(cookie)
            driver2_3.refresh()
            WebDriverWait(driver2_3, 5).until(EC.presence_of_element_located((By.ID, 'session')))
        except:
            driver2_3.find_element_by_name('session[username_or_email]').send_keys(t_email2)
            driver2_3.find_element_by_name('session[password]').send_keys(t_password2)
            driver2_3.find_element_by_name('remember_me').click()
            driver2_3.find_element_by_class_name('button.selected.submit').click()
            WebDriverWait(driver2_3, 5).until(EC.presence_of_element_located((By.ID, 'session')))
            pickle.dump(driver2_3.get_cookies() , open("cache/" + email2 + "/cookies_t.pkl","wb"))
        driver2_3.find_element_by_name('status').send_keys(" {0}".format(random.randint(1,999999999)))
        driver2_3.find_element_by_class_name('button.selected.submit').click()

        driver2_3.switch_to.window(parent_window2_3)
        time.sleep(30)


    sel = 1 #2アカウント時の交換用

    while True:
        if sel == 1:
            driver1_3.find_element_by_name('status').send_keys(" {0}".format(random.randint(1,999999999)))
            driver1_3.find_element_by_class_name('button.selected.submit').click()

            driver1_3.switch_to.window(parent_window1_3)
            driver1_3.refresh()

        if mode == 2 and sel == 2:
            driver2_3.find_element_by_name('status').send_keys(" {0}".format(random.randint(1,999999999)))
            driver2_3.find_element_by_class_name('button.selected.submit').click()

            driver2_3.switch_to.window(parent_window2_3)
            driver2_3.refresh()

        time.sleep(random.randint(25,60))
        if sel == 1 and mode == 2: sel = 2
        else:
            if sel == 2: sel = 1

        if sel == 1:
            driver1_3.find_element_by_class_name('Box__header__a').click()
            WebDriverWait(driver1_3, 5).until(lambda d: len(d.window_handles) > 1)
            driver1_3.switch_to.window(driver1_3.window_handles[1])

        if mode == 2 and sel == 2:
            driver2_3.find_element_by_class_name('Box__header__a').click()
            WebDriverWait(driver2_3, 5).until(lambda d: len(d.window_handles) > 1)
            driver2_3.switch_to.window(driver2_3.window_handles[1])
    """

    #ユーザー検索ページ接続 > シェアボタンクリック
    try:
        driver1_3.get('https://yay.space/users/search')
        WebDriverWait(driver1_3, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div[2]/div[1]/a')))
        parent_window1_3 = driver1_3.current_window_handle
    except:
        logging.error("Browser1_3 Connection timed out...!!")
        sys.exit()
    driver1_3.find_element_by_class_name('Box__header__a').click()
    WebDriverWait(driver1_3, 5).until(lambda d: len(d.window_handles) > 1)
    driver1_3.switch_to.window(driver1_3.window_handles[1])


    #Twitterログイン
    try:
        cookies = pickle.load(open("cache/" + email2 + "/cookies_t.pkl", "rb"))
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
                driver1_3.add_cookie(cookie)
        driver1_3.refresh()
        WebDriverWait(driver1_3, 5).until(EC.presence_of_element_located((By.ID, 'session')))
    except:
        driver1_3.find_element_by_name('session[username_or_email]').send_keys(t_email2)
        driver1_3.find_element_by_name('session[password]').send_keys(t_password2)
        driver1_3.find_element_by_name('remember_me').click()
        driver1_3.find_element_by_class_name('button.selected.submit').click()
        WebDriverWait(driver1_3, 5).until(EC.presence_of_element_located((By.ID, 'session')))
        pickle.dump(driver1_3.get_cookies() , open("cache/" + email2 + "/cookies_t.pkl","wb"))


    while alive:
        driver1_3.find_element_by_name('status').send_keys(" {0}".format(random.randint(1,999999999)))
        driver1_3.find_element_by_class_name('button.selected.submit').click()

        driver1_3.switch_to.window(parent_window1_3)
        driver1_3.refresh()

        time.sleep(random.randint(30,120))

        driver1_3.find_element_by_class_name('Box__header__a').click()
        WebDriverWait(driver1_3, 5).until(lambda d: len(d.window_handles) > 1)
        driver1_3.switch_to.window(driver1_3.window_handles[1])

#----------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    try:
        login()
        threading.Thread(target = auto_c).start()
        threading.Thread(target = main).start()
        threading.Thread(target = main_sub).start()
        #threading.Thread(target = auto_share).start()
        if config_ini.get('Mode', 'AutoPostComparison') == "True":
            if not os.path.exists("cache/" + email1 + "/comparison_date.json"):
                driver1_4.find_element_by_class_name('Header__profile').click()
                WebDriverWait(driver1_4, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[1]/div/div/div')))
                posts = driver1_4.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/div[1]/div/div[2]/dl/div[1]/a/dd').text
                follow = driver1_4.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/div[1]/div/div[2]/dl/div[4]/a/dd').text
                follower = driver1_4.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/div[1]/div/div[2]/dl/div[3]/a/dd').text
                letter = driver1_4.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/div[1]/div/div[2]/dl/div[2]/a/dd').text
                str = {"posts": int(posts.replace(",", "")), "likes": 0, "follow": int(follow.replace(",", "")), "follower": int(follower.replace(",", "")), "rt_to": 0, "rt_me": 0, "letter": int(letter.replace(",", "")), "yesterday_posts": 0, "yesterday_likes": 0, "yesterday_follow": 0, "yesterday_follower": 0, "yesterday_rt_to": 0, "yesterday_rt_me": 0, "yesterday_letter": 0}
                with open("cache/" + email1 + "/comparison_date.json", mode='w') as f:
                    json.dump(str, f, indent=2, ensure_ascii=False)
            threading.Thread(target = auto_conpari).start()

        thread_list = threading.enumerate()
        thread_list.remove(threading.main_thread())
        for thread in thread_list:
            thread.join()
    except KeyboardInterrupt:
        alive = False
        time.sleep(5)
        #Ctrl+Cによるプログラム強制終了によるブラウザ強制終了対策
        #ドライバーを終了させる
        logging.warning("KeyboardInterruptをキャッチしたため、ブラウザを強制終了します")
        driver1_1.quit()
        driver1_2.quit()
        driver1_3.quit()
        if mode == 2:
            driver2_1.quit()
            driver2_2.quit()
            driver2_3.quit()
        pass
