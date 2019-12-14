import argparse
import serial
from time import sleep
from datetime import timedelta
import calendar
from getch import getch, pause

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

    def manual(self):
        print('マニュアルモードに移行しました. キーボードでコントローラを操作できます. 終了する場合は^Cを押して下さい.')
        print('awds=LX, xfvc=HAT, ko;l=Button_YXAB, nj,m=RX, q=L, 1=ZL, p=R, -=ZR, g=SELECT, h=START, b=CAPTURE, <space>=HOME')
        while True:
            key = getch()

            button_duration = 0.05
            home_duration = 0.3
            stick_duration = 0.2
            hat_duration = 0.05

            if key == '\x03':
                raise KeyboardInterrupt()

            if key == 'a':
                self.send('LX MIN', stick_duration)
            if key == 'w':
                self.send('LY MIN', stick_duration)
            if key == 'd':
                self.send('LX MAX', stick_duration)
            if key == 's':
                self.send('LY MAX', stick_duration)

            if key == 'x':
                self.send('HAT LEFT', hat_duration)
            if key == 'f':
                self.send('HAT TOP', hat_duration)
            if key == 'v':
                self.send('HAT RIGHT', hat_duration)
            if key == 'c':
                self.send('HAT BOTTOM', hat_duration)

            if key == 'k':
                self.send('Button Y', button_duration)
            if key == 'o':
                self.send('Button X', button_duration)
            if key == ';':
                self.send('Button A', button_duration)
            if key == 'l':
                self.send('Button B', button_duration)

            if key == 'n':
                self.send('RX MIN', stick_duration)
            if key == 'j':
                self.send('RY MIN', stick_duration)
            if key == ',':
                self.send('RX MAX', stick_duration)
            if key == 'm':
                self.send('RY MAX', stick_duration)
            
            if key == 'q':
                self.send('Button L', button_duration)
            if key == '1':
                self.send('Button ZL', button_duration)
            
            if key == 'p':
                self.send('Button R', button_duration)
            if key == '-':
                self.send('Button ZR', button_duration)
            
            if key == 'g':
                self.send('Button SELECT', button_duration)
            if key == 'h':
                self.send('Button START', button_duration)
            
            if key == 'b':
                self.send('Button CAPTURE', button_duration)
            if key == ' ':
                self.send('Button HOME', home_duration)

            sleep(0.05)

