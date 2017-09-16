# 部署在臺南市飛番雲 IaaS 平台

## 設置 Python 執行環境 (virtualenv)
### 安裝必要軟體
```
$ apt-get install sqlite
$ apt-get install python-pybabel
$ apt-get install python-pip
$ apt-get install virtualenv
```
### 切換至 virtualenv 環境內
```
$ virtualenv --no-site-packages afc
$ cd afc/
$ source bin/activate
```
### 下載報名系統原始碼
```
$ git clone https://github.com/lyshie/afc-github
$ cd afc-github/ 
```

## 設定課後社團報名系統
[後續請參照說明文件的設定](https://github.com/lyshie/afc-github/tree/master#編輯設定檔)
