# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
#    こちらはセットアップのために使用します。原則、改変せずそのまま実行してご利用ください。
#    This is used for setup. In principle, please use it without modification.
#
#    Requirement / 動作条件 :
#    CentOS7 and Python3.x.x
#
# ----------------------------------------------------------------------
#
#    使用方法（how to use）:
#    1. Python3をインストール後、「python setup.py」と打ち込み実行します。
#       After installing Python3, type "python setup.py" and execute.
#    2. コンソールに表示される案内に沿ってください。
#       Follow the instructions displayed on the console.
# ----------------------------------------------------------------------

import sys, subprocess, os



# 挨拶と注意書き
print("Yay_BtClのご利用ありがとうございます。\nThank you for using Yay_BtCl.\n")
print("注意書き（Note）\n1. こちらのセットアップツールでは、Yay_BtClの利用に必要なパッケージ等を全て自動でインストールします。\n   This setup tool automatically installs all the packages etc. necessary for using Yay_BtCl.")
print("2. このセットアップツールによって、引き起こされた問題には責任を負いません。\n   We are not responsible for problems that occur with this setup tool.")
print("3. CentOS 7 向けに作成されたものであり、他OSには対応しておりません。\n   It was created for CentOS7 and does not support other OS.\n")
while True:
    y_n = input("同意してセットアップを続行しますか？（Agree and continue setup?） [y/n] : ")

    if y_n == "n":
        print("セットアップをキャンセルします。（Cancel setup.）")
        sys.exit()
    elif y_n == "y":
        break
    else:
        print("もう一度、実行してください。（Please try again.）\n")
        continue


# OSの判別
if os.name != 'posix':
    print("LinuxOS only.")
    sys.exit()


# 必要なパッケージをインストール
pk_install = subprocess.Popen(["yum", "-y", "install", "libX11", "GConf2", "fontconfig", "unzip", "wget"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#print(pk_install.stdout.decode("utf-8"))
while True:
    line = pk_install.stdout.readline()
    print(line.decode("utf-8"))
    if not line: break


# ChromeDriverのインストール
def CD_install():
    cmd_list = [["wget", "https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip"], ["unzip", "chromedriver_linux64.zip"], ["mv", "chromedriver", "/usr/local/bin/"], ["rm", "-r", "chromedriver_linux64.zip"], ["chmod", "755", "/usr/local/bin/chromedriver"]]
    for cmd in cmd_list:
        cd_install = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            line = cd_install.stdout.readline()
            print(line.decode("utf-8"))
            if not line: break
while True:
    y_n = input("ChromeDriverをインストールします。続行しますか？（Install ChromeDriver. Do you want to continue?） [y/n/S] : ")

    if y_n == "n":
        print("インストールをキャンセルします。（Cancel install.）")
        sys.exit()
    elif y_n == "y":
        CD_install()
        break
    elif y_n == "S":
        print("インストールをスキップします。（Skip install.）")
        break
    else:
        print("もう一度、実行してください。（Please try again.）\n")
        continue


# GoogleChromeのインストール
def GC_install():
    s = '''[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl.google.com/linux/linux_signing_key.pub
'''
    with open('/etc/yum.repos.d/google-chrome.repo', mode='w') as f:
        f.write(s)

    gc_install = subprocess.Popen(["yum", "-y", "install", "google-chrome-stable", "libOSMesa"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line = gc_install.stdout.readline()
        print(line.decode("utf-8"))
        if not line: break
while True:
    y_n = input("GoogleChromeをインストールします。続行しますか？（Install GoogleChrome. Do you want to continue?） [y/n/S] : ")

    if y_n == "n":
        print("インストールをキャンセルします。（Cancel install.）")
        sys.exit()
    elif y_n == "y":
        GC_install()
        break
    elif y_n == "S":
        print("インストールをスキップします。（Skip install.）")
        break
    else:
        print("もう一度、実行してください。（Please try again.）\n")
        continue


# ChromeDriver と GoogleChrome のバージョンを確認
print("\nChromeDriver と GoogleChrome のバージョンを確認します。\nWe will check the versions of ChromeDriver and GoogleChrome.\n")

cd_ver = subprocess.Popen(["chromedriver", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
while True:
    line = cd_ver.stdout.readline()
    print(line.decode("utf-8"))
    if not "ChromeDriver 80" in line.decode("utf-8") and line:
        if "ChromeDriver" in line.decode("utf-8"):
            print("ChromeDriverのバージョンが一致しないため、再構築が必要です。こちらのセットアップツールはご利用頂けません。\nChromeDriver versions do not match and need to be rebuilt.\nThis setup tool cannot be used.")
            sys.exit()
        else:
            print("ChromeDriverがインストールされていません。もう一度やり直してください。\nChromeDriver is not installed. Please try again.")
            sys.exit()
    if not line: break
gc_ver = subprocess.Popen(["google-chrome", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
while True:
    line = gc_ver.stdout.readline()
    print(line.decode("utf-8"))
    if not "Google Chrome 80" in line.decode("utf-8") and line:
        if "Google Chrome" in line.decode("utf-8"):
            print("GoogleChromeのバージョンが一致しないため、再構築が必要です。こちらのセットアップツールはご利用頂けません。\nGoogleChrome versions do not match and need to be rebuilt.\nThis setup tool cannot be used.")
            sys.exit()
        else:
            print("GoogleChromeがインストールされていません。もう一度やり直してください。\nGoogleChrome is not installed. Please try again.")
            sys.exit()
    if not line: break

print("ChromeDriver と GoogleChrome の正常なインストールが確認できました。\nI confirmed that ChromeDriver and GoogleChrome were installed properly.")

# Seleniumのインストール
def Sl_install():
    for cmd in cmd_list:
        sl_install = subprocess.Popen(["pip", "install", "selenium"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            line = sl_install.stdout.readline()
            print(line.decode("utf-8"))
            if not line: break
while True:
    y_n = input("Seleniumをインストールします。続行しますか？（Install Selenium. Do you want to continue?） [y/n/S] : ")

    if y_n == "n":
        print("インストールをキャンセルします。（Cancel install.）")
        sys.exit()
    elif y_n == "y":
        Sl_install()
        break
    elif y_n == "S":
        print("インストールをスキップします。（Skip install.）")
        break
    else:
        print("もう一度、実行してください。（Please try again.）\n")
        continue

# Seleniumのインストールを確認
print("\nSeleniumのインストールを確認します。\nWe will check the install of Selenium.\n")

sl_ver = subprocess.Popen(["pip", "show", "selenium"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
while True:
    line = sl_ver.stdout.readline()
    print(line.decode("utf-8"))
    if "Name: selenium" in line.decode("utf-8"):
        break
    if not line:
        print("Selenium のインストールが確認できないため、再構築が必要です。こちらのセットアップツールはご利用頂けません。\nRebuilding is required because the installation of Selenium cannot be confirmed.\nThis setup tool cannot be used.")

print("Selenium の正常なインストールが確認できました。\nI confirmed that Selenium were installed properly.")
print("\n\nセットアップを終了します。\nExit setup.")
