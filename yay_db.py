# -*- coding: utf-8 -*-
import os, time, pickle, sys, logging, re, configparser

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

email1 = config_ini.get('Account', 'email1')
password1 = config_ini.get('Account', 'password1')

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
driver1 = webdriver.Chrome(options=options)

#Yay!サーバー接続確認
try:
    logging.info("Browser1 Connection check...")
    driver1.get('https://yay.space/timeline/following')
    WebDriverWait(driver1, 5).until(EC.presence_of_all_elements_located)
    logging.info("Browser1 Connected successfully...")
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
            driver1.add_cookie(cookie)
        driver1.refresh()
        WebDriverWait(driver1, 5).until(EC.presence_of_all_elements_located)
        driver1.find_element_by_class_name('Header__profile__a')
        logging.info("Logged in to Account from saved information...")
    except:
        #ログインされていない場合
        try:
            logging.info("Browser1 Move page...")
            driver1.get('https://yay.space/login')
            WebDriverWait(driver1, 5).until(EC.presence_of_all_elements_located)
        except:
            logging.error("Browser1 Connection timed out...!!")
            sys.exit()

        #ログイン情報記入 > ログインボタンクリック
        logging.info("Browser1 Start login...")
        driver1.find_element_by_name('email').send_keys(email1)
        driver1.find_element_by_name('password').send_keys(password1)
        driver1.find_element_by_class_name('Button.Button--less-rounded.Button--icon-login').click()
        #ログイン読み込み待ち
        for _ in range(50):
            if driver1.current_url == "https://yay.space/timeline/following":
                break
            else:
                time.sleep(0.1)
        else:
            logging.error("Browser1 Connection timed out...!!")
            sys.exit()

        #ログインクッキー保存
        pickle.dump(driver1.get_cookies() , open("cache/" + email1 + "/cookies.pkl","wb"))
        logging.info("Browser1_1 Login completed...")

#----------------------------------------------------------------------------------------------------#

    #ログインユーザーのステータス
    my_id = driver1.find_element_by_class_name('Header__profile__a').get_attribute("href")
    my_name = driver1.find_element_by_class_name('Nickname__span').text
    try:
        driver1.find_element_by_class_name('ImageLoader.Avatar.Avatar--vip')
        d_vip = "Enable"
    except:
        d_vip = "Disable"

    logging.info("Login Status\n< Main Account >\nUSERID:["+my_id.replace("https://yay.space", "") + "] NAME:["+my_name + "] VIP:"+d_vip + "\n")

#----------------------------------------------------------------------------------------------------#

def main():
    # 最近ログインしたユーザーにページ移動
    driver1.get("https://yay.space/users/search")
    # 最近ログインしたユーザーから最上部のユーザーマイページに移動
    driver1.find_element_by_class_name('UserList__item').click()


#----------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    try:
        login()
        main()
    except KeyboardInterrupt:
        alive = False
        time.sleep(5)
        #Ctrl+Cによるプログラム強制終了によるブラウザ強制終了対策
        #ドライバーを終了させる
        logging.warning("KeyboardInterruptをキャッチしたため、ブラウザを強制終了します")
        driver1.quit()
