#!/usr/bin/env python3
import argparse
import serial
from time import sleep
from datetime import date

from lib.controller import Controller

# 1. 日付を2000/1/1に合わせる
# 2. W回収済み & 柱のある巣の前へ移動
# 3. ホームに戻り, コントローラ接続画面を開く
# 4. スクリプトを実行する

# ## スクリプトの書式
# ```
# $ ./scripts/get-w.py /dev/tty.usbserial*
# ```

parser = argparse.ArgumentParser()
parser.add_argument('port')
args = parser.parse_args()
ser = serial.Serial(args.port, 9600)
controller = Controller(ser, date(2000, 1, 1))

sleep(1)

# コントローラの接続
controller.register()

# ゲームに戻る
controller.back_game()
sleep(1) # ホームから直接フィールドの画面に戻るとラグが発生するので, 多めにsleepする

try:
    while True:
        # みんなで対戦を開く
        controller.send('Button A', 0.1)
        sleep(0.7)
        controller.send('Button A', 0.1)
        sleep(2) # ラグを考慮し, 多めにsleepしている

        # ホームに戻る
        controller.back_home()

        # 日付を進める
        controller.increment_date()

        # ゲームに戻る
        controller.back_game()

        # みんなで対戦を閉じる
        controller.send('Button B', 0.1)
        sleep(0.6)
        controller.send('Button A', 0.1)
        sleep(3.3) # フィールドを開いた直後のラグを考慮し, 多めにsleepしている

        # W回収
        controller.send('Button A', 0.1)
        sleep(0.3)
        controller.send('Button A', 0.1)
        sleep(0.3)
except KeyboardInterrupt:
    controller.send('RELEASE', 0)
    ser.close()
