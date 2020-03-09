<p align="center">
   <a href="https://yay.space/">
      <img src="Yay-logo.jpg" width="10%" alt="Yay_BtCl" />
   </a>
  <h1 align="center">データベース構築用 メモ</h1>
</p>

<p align="center">
※こちらはあくまで記録として残しているものであり、全ての構築を保証するものではありません。
</p>


## 収集する情報

### 1.プロフィール基本（users）
* 独自データID（id）
* ユーザーID（userid）
* 名前（name）
* アイコンURL（icon）
* カバーURL（cover）
### 2.プロフィール詳細（profiles)
* 独自データID（id）
* 投稿数（posts）
* レター（letters)
* サークル（circles）
* フォロワー（follower）
* 作成日時（created_at）
* 最終更新日時（updated_at）


## データベース作成
```sh
create database yay;
```

## データベース一覧より確認
```sh
show databases;

+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| yay                |
+--------------------+
```

## プロフィール基本（user_basic）テーブル作成
```sh
create table users (
    id int primary key,
    userid int not null unique,
    name varchar(255),
    icon varchar(255),
    cover varchar(255)
);
```

## プロフィール詳細（profiles)テーブル作成
```sh
create table profiles (
    id int primary key,
    posts int,
    letters int,
    circles int,
    follower int,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp
);
```
