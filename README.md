# hanken_public

![log](https://github.com/ruteru64/hanken_public/blob/main/img/logo_large.png)
©2022 HANKEN all rights reserved

https://www.youtube.com/watch?v=xHtXZEfri_U

## 前書き

セキュリティの関係から開発しているリポジトリではないリポジトリで公開いたします。

## 概要

今現在、開催されるイベントは入場時の本人確認に手間と時間がかかりすぎている問題があります。また、チケットの転売が横行し、チケットが本当に欲しい人の手に渡らない問題もあります。
その二つの課題を解決するために、SuicaやICOCAなどに使用されるNFCを使用し、入場時の本人確認を迅速に行いつつチケットの転売を抑止するチケット販売管理システムを私たちは開発しました。

2022年3月26日 DEMODAY オーディエンス賞・GMO賞受賞 W受賞

## サーバーについて

AWSにデプロイ済み
AWSの構成にはTerrafomを使用。
開発環境の構築としてDockerを使用。


## プロジェクトへの思い

チームメンバーの二人がイベントの主催をしたときにチケットの本人確認にものすごい時間がかかって大変だったという経験をもとに、イベント主催の時の本人確認などの入場処理を簡単にすることで今下火になっているイベントをより簡単に企画できるシステムを作成することになりました。実際にメンバーに起こった体験からヒントを得たものなのでより実感を持ちながら開発に取り組めたと思います。

## 工夫した点

* デプロイまで行った。
* DBの正規化を行うときにDBの規模を考え正規化を行った。
* NFCを扱った。
* androidアプリも作成した。
* 動作を早く行えるように調整を行った。
* タスク管理をしっかりと行った。
* Pay.jpを利用し決済処理まで行えるようにした。
* コンプライアンスに注意して開発を行った。


## リンク

### Web

https://hanken.link

### AndoridApp

https://play.google.com/store/apps/details?id=com.node.hanken_native

https://github.com/ruteru64/hanken_native


## 使用技術

* python
* Django
* React
* Java
* android
* SQLite
* NFC
* AWS
* GNU Make
* Go

### 選定理由

#### python
全員が使える言語であったため

#### Django
全員触れたことがないが簡単な開発を行えるため

#### React
DOMに関して管理ができないため一意な気泡として導入。CDN

#### JAVA
android開発をするときにNativな機能を使用したかったためKotlin or JAVAとなったが、JAVAの記法もままならないままKotlinに挑戦するのが時間的に難しかった

#### android,nfc
サービスのユーザー体験を上げるため

#### SQLite
メンバーが全員問題なく使用できるため

#### AWS
公開時にある程度自由にサーバーを構築できるため。あと無料枠

#### terraform
AWSの構成のために使用

#### Docker
開発環境の構成のために使用

#### GNU Make
実行コードが長くなったのでできる限り人的なミスを少なくするため

#### Go
最速でファイルサーバーを立ち上げたかった。あとコンパイルするから早そう


## ファイル構成

```
.
├── src(webのソースコード)
├── doc(webのドキュメント)
├── img(画像)
└── hanken_native(androidアプリのソースコード)

```

## 作業中(完成するかわからない)

画像ファイルサーバ
https://github.com/ruteru64/hanken_img_server
