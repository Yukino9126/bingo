# Bingo

A homework for Python Network Programming in NCNU.

## Description

本次 Bingo 程式共分成三個模組:

- `client()`:
    1. 啟動後, 請使用者輸入名字 (可包含空白, 以利輸入英文全名), 以及 5x5 個1到25的整數 (不可重覆). 輸入格式由程式自訂.
    2. client 端將送一個字串給server. 字串內容為26個欄位, 第一欄為使用者姓名, 接著是25個整數, 各欄之間以英文半形逗號隔開. 格式如"Helen Keller,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25".
    3. server端會回送兩個數字(中間以逗號隔開). 第一個數字表示該使用者是第幾位加入遊戲的玩家, 第二個數字表示預計幾秒鐘後遊戲會開始.
    4. 當 client 收到 server 送來 "Start" 字串後, 遊戲正式開始. (可能和之前預告的秒數有出入. 大夥兒都知道, 即使約好時間, 也不保證能準時開始.)
    5. 接著 client 進入一個迴圈:
        1. 由 server 接收一個字串.
        2. 若該字串為"Bingo" 開頭, 代表有其他玩家已達到 Bingo 的條件. 遊戲結束.
        3. 若該字串為整數. 判斷是否達到 Bingo 的條件. 若已達到, 就送 "Bingo" 給 server. 遊戲結束.
- `server()`:
    1. 進入一個迴圈, 等待 client 端加入遊戲.
        1. Client端送來格式為 "Alice,1,2,3,...,25" 的字串.
        2. Server端回應格式略為 "3,20" 的字串 (第3位; 預計20秒後開始).
        3. 離開迴圈的條件由server端自訂.
    2. 廣播 "Start" 字串給所有 client.
    3. 產生一個1到25的list. 將次序混排 (shuffle).
    4. 進入一個迴圈,
        1. 依序每次送出一個list中的整數.
        2. 等待有使用者送來 "Bingo".
        3. 若一段時間(如: 2.0秒)後無人喊 "Bingo", 則 time-out.
        4. 若有人喊 "Bingo", 但其實尚未達 Bingo 條件, 回覆他 "You are wrong."
        5. 若喊的人真的 Bingo, 廣播 "Bingo,Alice from 163.28.xxx.yyy" 給所有人. 離開迴圈.
    5. 遊戲結束.
- `checkBingo(clientBoard, currentList)`:
    1. clientBoard 為 5x5 之棋盤, currentList 為 server 到目前為止送出的數字集(可能少於25個).
    2. 回傳值為 True 或 False.

## Usage

### server

```bash
python3 main.py server -p [port] [host]
```

### client

```bash
python3 main.py client -p [port] [host]
```