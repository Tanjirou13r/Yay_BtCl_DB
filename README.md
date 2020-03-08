<p align="center">
   <a href="https://yay.space/">
      <img src="Yay-logo.jpg" width="10%" alt="Yay_BtCl" />
   </a>
  <h1 align="center">Yay_BtCl_DB</h1>
</p>

<p align="center">
      <a href="https://travis-ci.com/TanakashiXr/Yay_BtCl_DB"><img alt="Build Status" src="https://travis-ci.com/TanakashiXr/Yay_BtCl_DB.svg?token=hQziw2chDyu4Ysu1ptd9&branch=master" /></a>
      <a href="https://github.com/TanakashiXr/Yay_BtCl_DB"><img alt="release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/TanakashiXr/Yay_BtCl_DB?include_prereleases" /></a>
      <a href="https://github.com/TanakashiXr/Yay_BtCl_DB/blob/master/LICENSE"><img alt="LICENSE" src="https://img.shields.io/badge/License-MIT%20License-blue.svg" /></a>
      <a href="https://www.python.org/downloads/"><img alt="Supported python versions: 3.x.x" src="https://img.shields.io/badge/Python-3.x.x-green.svg" /></a>
</p>

<p align="center">
こちらは当ソースコードの説明になります。ご使用前に必ずご覧ください。<br>
This is the description of this source code. Please read before use.
</p>

## Requirement / 動作条件

* Python 3.x.x
* Selenium 3.x.x
* ChromeDriver 80.x.x.x
* Google Chrome 80.x.x.x

## Install / インストール

当プログラムを使用するには上記、動作条件を満たす必要があります。  
To use this program, you must meet the above requirements.

Python3のインストールは各自で、行ってください。それ以降の構築は、「setup.py」より自動で行えます。  
Please install Python3 by yourself. Subsequent construction can be performed automatically from "setup.py".

当ソースコードをダウンロードし、解凍します。  
Download and unzip this source code.
Install Selenium.
```sh
$ git clone https://github.com/TanakashiXr/Yay_BtCl_DB.git
$ cd Yay_BtCl_DB
$ python setup.py
```

## Usage / 使用方法

各自の環境に合わせ、「config.ini」の編集を行ってください。  
Edit according to your environment.
```sh
$ cp config_template.ini config.ini
$ vi config.ini
$ python yay_db.py
```

## Features / 機能

* ユーザー情報を取得してデータベースへ登録

## Author / 作者

* たなか氏

## License / ライセンス

このソフトウェアは、MITライセンスの下でリリースされています。ライセンスを参照してください。  
This software is released under the MIT License, see LICENSE.
