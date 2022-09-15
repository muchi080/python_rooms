import requests
from bs4 import BeautifulSoup
from datetime import datetime
import schedule
from time import sleep
import csv
import re

logList = []
header = ['時間', '部屋数', '部屋番号','状態']
# with open('test.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(header)

i = 0

#01 定期実行する関数を準備
def job():
    url = "https://hotel-victoriacourt.com/vicy/vacancy/"
    global i
    r= requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    #部屋数
    counter =soup.find('div')
    s = counter.text.replace('\n','')
    counter_t = (s[:4] + '/' + s[4:])
    counter_t

    #時刻
    time = soup.find(class_='timestamp')
    t = time.text
    time_ = (t[:0]+t[:16])
    time_t = time_.replace('2022/','')

    #部屋番号
    rooms = soup.find(id='rooms')
    rooms_ = rooms.text.replace('\n',' ')
    rooms_t = rooms_.replace('\t','')
    
    

    #LINE自動送信
    message = f'\n{time_t}\n{counter_t}\n{rooms_t}\n https://hotel-victoriacourt.com/vicy/vacancy/'
    def send_line_notify(message):
        # コピーしたトークンを貼り付けてください
        line_notify_token = '9FYWyVjpJeFmSLMc0GVkd5H0XW7Y9oTjtsKMiS3z2Ri'
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {line_notify_token}'}
        data = {'message': message}
        requests.post(line_notify_api, headers = headers, data = data)
    


    #701号室チェック
    if '701' in rooms_t:
        send_line_notify(message)
        j = "成功"
        print(time_t)
        print(j)
    else:
        j = "空いてない(´・ω・)"
        print(time_t)
        print(j)
    #     i +=1
    #     if i ==12:
    #         i = 0
    #         print('送信')
    #         send_line_notify(message)

        
        
    #csv書き込み
    log = [] 
    log.append([time_t, counter_t, rooms_t, j])
    with open('test.csv', 'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerows(log)

  
#定期実行
schedule.every(5).minutes.do(job) 
while True:
    schedule.run_pending()
    sleep(2)