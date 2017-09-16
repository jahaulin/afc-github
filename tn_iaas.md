# 部署在臺南市飛番雲 IaaS 平台

## 設置 Python 執行環境 (virtualenv)
```
$ apt-get install sqlite
$ apt-get install python-pybabel
$ apt-get install python-pip
$ apt-get install virtualenv

$ virtualenv --no-site-packages afc
$ cd afc/
$ source bin/activate

$ git clone https://github.com/lyshie/afc-github
$ cd afc-github/ 
```

## 設定課後社團報名系統
[後續請參照說明文件的設定](https://github.com/lyshie/afc-github/tree/master#編輯設定檔)
