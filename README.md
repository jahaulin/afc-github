# afc-github
國小階段課後社團報名系統，提供學生家長線上報名使用。管理者可自行匯入「學生」與「課程」資料，進行編輯與管理；學生家長可線上進行「選課」。


## 1. 系統資訊
  - GNU/Linux，如 CentOS、Fedora、Debian 等
  - SQLite3
```bash
# dnf install sqlite
```
  - Python 2.7 以上，及如下模組
```
alembic
Flask
Flask_Babel
Flask_Login
Flask_Migrate
Flask_Script
Flask_SQLAlchemy
Flask_WTF
pytz
SQLAlchemy
Werkzeug
WTForms
```


## 2. 程式安裝

### 下載原始碼
```bash
# git clone https://github.com/lyshie/afc-github
```

### 編輯設定檔
```bash
# cd afc-github/
# touch app/config.py
# vim config.py
# vim app/config.py
```
```
RECAPTCHA_PUBLIC_KEY = ""    # 沒有申請就不用填
RECAPTCHA_PRIVATE_KEY = ""   # 沒有申請就不用填
```

### 安裝 Python 相關模組
```bash
# pip install --upgrade --user -r requirements.txt
```

### 建立初始資料庫
```bash
# cd afc-github/
# sqlite3 app.db < afc.sql
```

### 建立管理者
```bash
# cd afc-github/
# vim app/scripts/db_create_admin.py
```
```
user.uid = 0                        # 'uid = 0' 是管理者
user.student_grade    = 6           # 管理者虛擬年級
user.student_class    = 6           # 管理者虛擬班級
user.student_number   = 99          # 管理者虛擬座號
user.student_name     = "admin"     # 管理者姓名
user.default_password = "PaSSwoRD"  # 管理者密碼
```
```bash
# ./app/scripts/db_create_admin.py
```

### 產生語系翻譯檔(中文正體)
```bash
# cd afc-github/
# ./tr_update.sh
```

### 測試執行
開啟瀏覽器，連結至 [http://127.0.0.1:5000/](http://127.0.0.1:5000/)，嘗試以管理者帳號登入。
```bash
# cd afc-github/
# ./run.py
```
```
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with inotify reloader
 * Debugger is active!
 * Debugger pin code: 316-959-504
```

### 使用者、課程設定

### 新增選課測試資料


## 3. 參考資訊
  - HSIEH, Li-Yi @ [臺南市進學國小資訊組](http://www.chps.tn.edu.tw/)
  - All programs are released under the GPL.
  - Free icons from [www.flaticon.com](http://www.flaticon.com/) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/)
