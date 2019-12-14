import argparse
import serial
from time import sleep
from datetime import timedelta
import calendar

class Controller:
    def __init__(self, ser, date, back_game_duration=0.9, back_home_duration=0.9):
        self.ser = ser
        self.date = date
        self.back_game_duration = back_game_duration
        self.back_home_duration = back_home_duration

    def send(self, msg, duration):
        print(msg)
        self.ser.write(f'{msg}\r\n'.encode('utf-8'))
        sleep(duration)
        self.ser.write(b'RELEASE\r\n')
    
    # コントローラを登録する
    # 事前条件: コントローラ接続画面を開いている
    # 事後条件: ホーム画面を開いている
    def register(self):
        self.send('Button L', 0.05)
        self.send('Button R', 0.05)
        sleep(1)
        self.back_home()

    # ゲームに戻る
    # 事前条件: ホーム画面を開いている
    # 事後条件: ゲーム画面を開いている
    def back_game(self, back_game_duration=None):
        self.send('Button HOME', 0.3) # ホームボタンは他のボタンと違って多めにdurationを取る必要がある
        sleep(back_game_duration if back_game_duration != None else self.back_game_duration)

    # ホームに戻る
    # 事前条件: ゲーム画面を開いている
    # 事後条件: ホーム画面を開いている
    def back_home(self, back_home_duration=None):
        self.send('Button HOME', 0.3) # ホームボタンは他のボタンと違って多めにdurationを取る必要がある
        sleep(back_home_duration if back_home_duration != None else self.back_home_duration)

    # 日付を進める
    # 事前条件: ホーム画面を開いている
    # 事後条件: ホーム画面を開いている
    def increment_date(self):
        # 設定を開く
        self.send('HAT RIGHT', 0.05)
        sleep(0.05)
        self.send('HAT RIGHT', 0.05)
        sleep(0.05)
        self.send('HAT BOTTOM', 0.05)
        sleep(0.05)
        self.send('HAT RIGHT', 0.05)
        sleep(0.05)
        self.send('Button A', 0.05)
        sleep(1)

        # 本体設定を開く
        self.send('HAT BOTTOM', 1.15)
        sleep(0.05)
        self.send('Button A', 0.05)
        sleep(0.05)

        # 日付と時刻を開く
        self.send('HAT BOTTOM', 0.05)
        sleep(0.05)
        self.send('HAT BOTTOM', 0.05)
        sleep(0.05)
        self.send('HAT BOTTOM', 0.05)
        sleep(0.05)
        self.send('HAT BOTTOM', 0.05)
        sleep(0.05)
        self.send('Button A', 0.05)
        sleep(0.2)

        # 現在の日付と時刻を開く
        self.send('HAT BOTTOM', 0.05)
        sleep(0.05)
        self.send('HAT BOTTOM', 0.05)
        sleep(0.05)
        self.send('Button A', 0.05)
        sleep(0.1)

        # 現在の日付と時刻を変更
        next_date = self.date + timedelta(days=1)
        ## 年
        if self.date.year != next_date.year:
            self.send('HAT TOP', 0.05) # 年を増やす
            sleep(0.05)
        self.send('HAT RIGHT', 0.05)
        sleep(0.05)
        ## 月
        if self.date.month != next_date.month:
            self.send('HAT TOP', 0.05) # 月を増やす
            sleep(0.05)
        self.send('HAT RIGHT', 0.05)
        sleep(0.05)
        ## 日
        if self.date.day + 1 != next_date.day:
            last_day_of_current_month = calendar.monthrange(self.date.year, self.date.month)[1]
            last_day_of_next_month = calendar.monthrange(next_date.year, next_date.month)[1]
            # 次の月の日数が現在の月よりも多いならその差だけ日付を進める
            for _i in range(last_day_of_next_month - last_day_of_current_month):
                self.send('HAT TOP', 0.05)
                sleep(0.05)
        self.send('HAT TOP', 0.05) # 1日に戻す
        sleep(0.05)
        self.send('HAT RIGHT', 0.05)
        sleep(0.05)
        # 時
        self.send('HAT RIGHT', 0.05)
        sleep(0.05)
        # 分
        self.send('HAT RIGHT', 0.05)
        sleep(0.05)
        # 決定
        self.send('Button A', 0.05)
        sleep(0.05)
        # date を更新
        self.date = next_date
        print(f'update date: {self.date}')
        
        # 現在の日付と時刻からホームに戻る
        self.back_home()
